"""
#   Name

txutil

#   Status

This library is considered production ready.

#   Description

A collection of helper functions to implement transactional operations.

#   Exceptions

##  CASConflict

**syntax**:
`CASConflict()`

User should raise this exception when a CAS conflict detect in a user defined
`set` function.

"""

# from .proc import CalledProcessError
# from .proc import ProcError

from .txutil import (
    CASConflict,
    cas_loop,
)

__all__ = [
    "CASConflict",
    "cas_loop",
]


def __getattr__(name: str) -> str:
    # importlib.metadata takes about 20 ms to import, so it is loaded only
    # when __version__ is read
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from importlib.metadata import version

    return version("k3txutil")
