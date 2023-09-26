from lpython import (dataclass, InOut, i32,
                     # print,
                     # str, list, Union, bool
    )
from lasr_stringio import (StringIO, __post_init__,
                           tell, read, seek,
                           SEEK_SET, SEEK_CUR, SEEK_END)


@dataclass
class LasrLexer:
    fd   : StringIO = StringIO('', 0, 0) # prefer Optional[StringIO]
    line : i32 = 1 # prefer Line
    col  : i32 = 1 # prefer Col
    type : str = '' # prefer LTType
    val  : str = '' # prefer LTVal


def _cons_res(self : LasrLexer,
              tt : str,
              v  : str) -> \
        tuple[i32,  # line
              i32,  # col
              str,  # LTType
              str,  # LTVal
              ]:
    result : tuple[i32, i32, str, str] = \
        self.line, self.col, tt, v
    return result


def next(self : InOut[LasrLexer]) -> \
    tuple[i32,  # line
          i32,  # col
          str,  # LTType
          str,  # LTVal
    ] :
    result : tuple[i32, i32, str, str] = -1, -1, '', ''
    s : str = '' # get_non_white(self)
    result = _cons_res(self, "int", s)
    return result


if __name__ == '__main__':
    lexer : LasrLexer = LasrLexer() # Issue #1991; dummy value
    lexer = LasrLexer(StringIO('(Integer 4 [])'))
    __post_init__(lexer.fd)
    line : i32
    col  : i32
    tokt : str
    tokv : str
    line, col, tokt, tokv = next(lexer)
    assert line == 1
