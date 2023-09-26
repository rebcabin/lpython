# from dataclasses import dataclass
# i32 = int
# from typing import \
#     Generic, TypeVar, Optional, Union, \
#     Tuple, Any, List, Pattern
# T_ = TypeVar('T_')
# class InOut(Generic[T_]):
#     pass


@dataclass
class StringIO:
    _buf     : str
    _0cursor : i32 = i32(0)
    _len     : i32 = i32(0)


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'
    fd   : StringIO = StringIO(integer_asr)
    assert fd._len == 0
    assert fd._0cursor == 0
