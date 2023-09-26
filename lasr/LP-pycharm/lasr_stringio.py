from lpython import dataclass, InOut, i32
# from typing import \
#     Generic, TypeVar, Optional, Union, \
#     Tuple, Any, List, Pattern


# Issue 1942
# from lasr_stringio import StringIO, read, tell, seek, SEEK_SET, __post_init__


# import re
# Only dataclass decorated classes and Enum subclasses are supported.
# @dataclass
# class IOBase:

#     def read(requested_bytes: int):
#         raise NotImplementedError


#  ___ _       _           ___ ___
# / __| |_ _ _(_)_ _  __ _|_ _/ _ \
# \__ \  _| '_| | ' \/ _` || | (_) |
# |___/\__|_| |_|_||_\__, |___\___/
#                    |___/


@dataclass
class StringIO:
    _buf     : str
    # Issue #1981
    _0cursor : i32 = 0  # i32(0)
    _len     : i32 = 0  # i32(0)


# Issue #1930: InOut type


def __post_init__(self: InOut[StringIO]):
    """Should be a member method of 'StringIO'.
    Imitate the behavior of Python 3.10.2 io library."""
    stringio_debug_dump(self, 'preconditions')
    self._len = len(self._buf)
    stringio_debug_dump(self, 'postconditions')


def stringio_debug_dump(self : StringIO, sigil : str):
    return
    print('StringIO __post_init__ ' + sigil + ':')
    print('    _buf = "', end='')
    print(self._buf, end='')
    print('".')
    print('    _len = ', end='')
    print(self._len, end='')
    print('.')
    print('    _0cursor = ', end='')
    print(self._0cursor, end='')
    print('.')


def tell(self: InOut[StringIO]) -> i32:
    """Should be a member method of 'StringIO'.
    Imitate the behavior of Python 3.10.2 io library."""
    result : i32 = self._0cursor
    return result


def read(self: InOut[StringIO], chars : i32) -> str:
    """Should be a member method of 'StringIO'.
    Imitate the behavior of Python 3.10.2 io library.
    On any negative number, read from cursor to end."""
    result : str = ''  # EOF
    if chars < 0:
        result = self._buf[self._0cursor : self._len]
        self._0cursor = self._len
    else:
        mac: i32 = min(self._len, self._0cursor + chars)
        assert mac <= self._len  # check 'min'
        result = self._buf[self._0cursor : mac]
        # Python 3.10.2 is observed NOT to reset cursor to 'mac'
        # if cursor is > mac! Subsequent tells will report a
        # value that is too large!
        if mac <= self._len:
            self._0cursor = mac
    return result


# Issue #1939: 'Literal' type hint


SEEK_SET : i32 = 0
SEEK_CUR : i32 = 1
SEEK_END : i32 = 2


def seek(self: InOut[StringIO], offset: i32, whence : i32) -> i32:
    """Imitate the behavior of Python 3.10.2 io library."""
    pos : i32 = 0
    if whence == SEEK_SET:
        pos = offset
    elif whence == SEEK_CUR:
        pos = self._0cursor + offset
    elif whence == SEEK_END:
        pos = self._len + offset
    else:
        raise ValueError(f"""Invalid whence ({whence}, should be 0, 1, or 2""")
    if (pos < 0):
        raise ValueError(f"""Negative seek position {pos}""")
    # Python 3.10.2 permits seeking beyond the end of the file!
    self._0cursor = pos
    return pos
