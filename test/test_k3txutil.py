import copy
import threading
import unittest

import k3thread
import k3ut

import k3txutil

dd = k3ut.dd


class MyError(Exception):
    pass


class TestCASLoop(unittest.TestCase):
    def setUp(self):
        self.lock = threading.RLock()
        self.val = 0
        self.ver = 0

    def tearDown(self):
        pass

    def _get(self):
        with self.lock:
            return self.val, self.ver

    def _set(self, val, prev_stat):
        with self.lock:
            if prev_stat != self.ver:
                raise k3txutil.CASConflict(prev_stat, self.ver)
            self.val = val
            self.ver += 1

    def _set_raise_myerror(self, val, prev_stat):
        with self.lock:
            raise MyError(prev_stat, self.ver)

    def test_cas(self):
        i = 0
        for curr in k3txutil.cas_loop(self._get, self._set):
            self.assertEqual(i, curr.stat)
            curr.v += 2

    def test_cas_n(self):
        for i, curr in enumerate(k3txutil.cas_loop(self._get, self._set_raise_myerror, conflicterror=MyError)):
            self.assertEqual(i, curr.n)
            if i == 4:
                break

    def test_cas_abort(self):
        for curr in k3txutil.cas_loop(self._get, self._set):
            curr.v += 2
            break

        self.assertEqual((0, 0), (self.val, self.ver))

    def test_cas_customed_error(self):
        for curr in k3txutil.cas_loop(self._get, self._set_raise_myerror, conflicterror=MyError):
            curr.v += 2
            if curr.n == 5:
                break

        self.assertEqual((0, 0), (self.val, self.ver))

    def test_cas_argument(self):
        rst = {}

        def _get(*args, **kwargs):
            rst["get"] = args, kwargs
            return "val", "stat"

        def _set(*args, **kwargs):
            rst["set"] = args, kwargs

        for curr in k3txutil.cas_loop(_get, _set, ("foo", "bar"), {"a": 1, "b": 2}):
            curr.v = "uservalue"

        self.assertEqual((("foo", "bar"), {"a": 1, "b": 2}), rst["get"])
        self.assertEqual((("foo", "bar", "uservalue", "stat"), {"a": 1, "b": 2}), rst["set"])

        # empty arg

        rst = {}

        for curr in k3txutil.cas_loop(_get, _set):
            curr.v = "uservalue"

        self.assertEqual(((), {}), rst["get"])
        self.assertEqual((("uservalue", "stat"), {}), rst["set"])

    def test_cas_concurrent(self):
        # Both threads read version 0 before either sets, so exactly one of them conflicts and retries once.
        barrier = threading.Barrier(2)
        last_n = []

        def _update():
            for curr in k3txutil.cas_loop(self._get, self._set):
                if curr.n == 0:
                    barrier.wait()
                curr.v += 1
            last_n.append(curr.n)

        ths = [k3thread.daemon(_update) for _ in range(2)]

        for th in ths:
            th.join()

        self.assertEqual((2, 2), (self.val, self.ver))
        self.assertEqual([0, 1], sorted(last_n))

    def test_cas_setter_error(self):
        # An error that is not a conflict ends the loop after one attempt.
        def _set(val, prev_stat):
            raise ValueError("foo")

        ns = []
        with self.assertRaises(ValueError):
            for curr in k3txutil.cas_loop(self._get, _set):
                ns.append(curr.n)
                curr.v += 1

        self.assertEqual([0], ns)

    def test_cas_nested_value_is_copied(self):
        stored = {"a": {"b": 1}}
        set_args = []

        def _get():
            return stored, "stat"

        def _set(val, prev_stat):
            set_args.append((val, prev_stat, copy.deepcopy(stored)))

        for curr in k3txutil.cas_loop(_get, _set):
            curr.v["a"]["b"] = 2

        self.assertEqual([({"a": {"b": 2}}, "stat", {"a": {"b": 1}})], set_args)

    def test_cas_setter_args_on_conflicts(self):
        # The setter conflicts twice, and the value and version change between tries.
        set_args = []

        def _set(val, prev_stat):
            set_args.append((val, prev_stat))
            if len(set_args) <= 2:
                self.val += 10
                self.ver += 1
                raise k3txutil.CASConflict()
            self.val = val
            self.ver += 1

        for curr in k3txutil.cas_loop(self._get, _set):
            curr.v += 1

        self.assertEqual([(1, 0), (11, 1), (21, 2)], set_args)
        self.assertEqual((21, 3), (self.val, self.ver))
