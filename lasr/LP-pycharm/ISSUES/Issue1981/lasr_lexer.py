from lpython import (dataclass, InOut, i32,)
from lasr_stringio import (StringIO, __post_init__,)


NEWLINE      : str       = "\n"
WHITESPACE   : list[str] = [" ", ",", NEWLINE, "\r", "\t"]
EOF_SIGNAL   : str       = ''


@dataclass
class LasrLexer:
    fd   : StringIO = StringIO('', 0, 0) # prefer Optional[StringIO]
    line : i32 = 1 # prefer Line
    col  : i32 = 1 # prefer Col
    type : str = '' # prefer LTType
    val  : str = '' # prefer LTVal


def lexer_test():
    print('LEXER TEST')
    lexer : LasrLexer = LasrLexer(StringIO('  foo  bar  '))
    __post_init__(lexer.fd)


if __name__ == '__main__':
    lexer_test()


