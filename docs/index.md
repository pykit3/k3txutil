# k3txutil

[![Action-CI](https://github.com/pykit3/k3txutil/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3txutil/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3txutil/badge/?version=stable)](https://k3txutil.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3txutil)](https://pypi.org/project/k3txutil)

Compare-and-swap (CAS) loop utilities for implementing transactional operations with optimistic concurrency control.

k3txutil is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

```bash
pip install k3txutil
```

## Quick Start

```python
import k3txutil

# Simple counter with CAS
data = {'value': 0, 'version': 0}

def getter():
    return data['value'], data['version']

def setter(new_val, old_version):
    if data['version'] != old_version:
        raise k3txutil.CASConflict()
    data['value'] = new_val
    data['version'] += 1

# Increment with retry on conflict
for rec in k3txutil.cas_loop(getter, setter):
    rec.v += 1
```

## API Reference

::: k3txutil

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
