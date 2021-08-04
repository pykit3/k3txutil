# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3txutil",
    packages=["k3txutil"],
    version="0.1.0",
    license='MIT',
    description='A collection of helper functions to implement transactional operations.',
    long_description='# k3txutil\n\n[![Action-CI](https://github.com/pykit3/k3txutil/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3txutil/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3txutil.svg?branch=master)](https://travis-ci.com/pykit3/k3txutil)\n[![Documentation Status](https://readthedocs.org/projects/k3txutil/badge/?version=stable)](https://k3txutil.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3txutil)](https://pypi.org/project/k3txutil)\n\nA collection of helper functions to implement transactional operations.\n\nk3txutil is a component of [pykit3] project: a python3 toolkit set.\n\n\n#   Name\n\ntxutil\n\n#   Status\n\nThis library is considered production ready.\n\n#   Description\n\nA collection of helper functions to implement transactional operations.\n\n#   Exceptions\n\n##  CASConflict\n\n**syntax**:\n`CASConflict()`\n\nUser should raise this exception when a CAS conflict detect in a user defined\n`set` function.\n\n\n\n\n# Install\n\n```\npip install k3txutil\n```\n\n# Synopsis\n\n```python\n\nimport k3txutil\nimport threading\n\n\nclass Foo(object):\n\n    def __init__(self):\n        self.lock = threading.RLock()\n        self.val = 0\n        self.ver = 0\n\n    def _get(self, db, key, **kwargs):\n        # db, key == \'dbname\', \'mykey\'\n        with self.lock:\n            return self.val, self.ver\n\n    def _set(self, db, key, val, prev_stat, **kwargs):\n\n        # db, key == \'dbname\', \'mykey\'\n        with self.lock:\n            if prev_stat != self.ver:\n                raise k3txutil.CASConflict(prev_stat, self.ver)\n\n            self.val = val\n            self.ver += 1\n\n    def test_cas(self):\n        for curr in k3txutil.cas_loop(self._get, self._set, args=(\'dbname\', \'mykey\', )):\n            curr.v += 2\n\n        print((self.val, self.ver)) # (2, 1)\n\nwhile True:\n    curr_val, stat = getter(key="mykey")\n    new_val = curr_val + \':foo\'\n    try:\n        setter(new_val, stat, key="mykey")\n    except CASConflict:\n        continue\n    else:\n        break\n\n#`cas_loop` simplifies the above workflow to:\nfor curr in k3txutil.cas_loop(getter, setter, args=("mykey", )):\n    curr.v += \':foo\'\n\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3txutil',
    keywords=['python', 'CASRecord'],
    python_requires='>=3.0',

    install_requires=['k3ut<0.2,>=0.1.15', 'k3thread<0.2,>=0.1.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3'],
)
