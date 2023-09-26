from lpython import dataclass, InOut, i32


@dataclass
class StringIO:
    _buf     : str
    _0cursor : i32 = i32(0)
    _len     : i32 = i32(0)


def __post_init__(this: InOut[StringIO]):
    """Should be a member method of 'StringIO'.
    Imitate the behavior of Python 3.10.2 io library."""
    print('StringIO __post_init__ preconditions:')
    print('    _buf = ', end='')
    print(this._buf, end='')
    print('.')
    print('    _len = ', end='')
    print(this._len, end='')
    print('.')
    print('    _0cursor = ', end='')
    print(this._0cursor, end='')
    print('.')
    this._len = len(this._buf)
    print('StringIO __post_init__ postconditions:')
    print('    _buf = ', end='')
    print(this._buf, end='')
    print('.')
    print('    _len = ', end='')
    print(this._len, end='')
    print('.')
    print('    _0cursor = ', end='')
    print(this._0cursor, end='')
    print('.')

