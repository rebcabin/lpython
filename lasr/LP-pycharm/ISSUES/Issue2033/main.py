from lpython import InOut


from lasr_stringio import (StringIO, __post_init__,
                           read, seek, tell, SEEK_SET)

from lasr_lexer import regex_test, lexer_test


def read_seek_tell_test(fd : InOut[StringIO]):
    print('READ-SEEK-TELL-TEST')
    a_char: str = read(fd, 1)
    assert a_char == '(', "a_char == '('"
    a_char = read(fd, 1)
    assert a_char == 'I', "a_char == 'I'"
    assert tell(fd) == 2, "tell(fd) == 2"
    assert seek(fd, 0, SEEK_SET) == 0
    assert seek(fd, 100, SEEK_SET) == 100
    assert seek(fd, 2, SEEK_SET) == 2
    temp: str = read(fd, -1)  # reads all the rest
    assert temp == 'nteger 4 [])'
    assert tell(fd) == 14


def stringio_test(fd : InOut[StringIO], integer_asr : str):
    print('STRINGIO TEST')
    assert fd._buf == integer_asr, "fd._buf == integer_asr"
    assert fd._len == len(integer_asr), "fd._len == len(integer_asr)"
    read_seek_tell_test(fd)


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'

    fd   : StringIO = StringIO(integer_asr)
    __post_init__(fd)  # Issue #1929

    stringio_test(fd, integer_asr)
    regex_test()
    lexer_test() # lexer)
