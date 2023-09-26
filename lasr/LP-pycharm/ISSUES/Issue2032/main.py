from lasr_stringio import StringIO, __post_init__
from lasr_lexer import stringio_test, regex_test, lexer_test


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'

    fd   : StringIO = StringIO(integer_asr)
    __post_init__(fd)  # Issue #1929

    stringio_test(fd, integer_asr)
    regex_test()
    lexer_test() # lexer)


