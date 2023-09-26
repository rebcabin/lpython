from lpython import (dataclass, InOut, i32,
                     # field, default_factory,
                     # print,
                     # str, list, Union, bool
    )
from lasr_stringio import (StringIO, __post_init__,
                           tell, read, seek,
                           SEEK_SET, SEEK_CUR, SEEK_END)


# import re
# Only dataclass decorated classes and Enum subclasses are supported.
# @dataclass
# class IOBase:

#     def read(requested_bytes: int):
#         raise NotImplementedError


# Issue #1930: InOut type


#  ___ _       _           ___ ___    _          _
# / __| |_ _ _(_)_ _  __ _|_ _/ _ \  | |_ ___ __| |_
# \__ \  _| '_| | ' \/ _` || | (_) | |  _/ -_|_-<  _|
# |___/\__|_| |_|_||_\__, |___\___/   \__\___/__/\__|
#                    |___/


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


#  ___
# | _ \___ __ _ _____ __
# |   / -_) _` / -_) \ /
# |_|_\___\__, \___/_\_\
#         |___/


NEWLINE      : str       = "\n"
WHITESPACE   : list[str] = [" ", ",", NEWLINE, "\r", "\t"]
RDR_MACROS   : list[str] = ["#_", "#'", "#:"]


LIST_OPEN    : str       = "("
VECT_OPEN    : str       = "["
HMAP_OPEN    : str       = "{"
HSET_OPEN    : str       = "#{"
COLL_OPENERS : list[str] = [LIST_OPEN, VECT_OPEN,
                            HMAP_OPEN, HSET_OPEN]

LIST_CLOSE   : str       = ")"
VECT_CLOSE   : str       = "]"
HASH_CLOSE   : str       = "}"  # for both HMAP & HSET
COLL_CLOSERS : list[str] = [LIST_CLOSE, VECT_CLOSE, HASH_CLOSE]

EOF_SIGNAL   : str       = ''


hexit         : str = r'[0-9a-fA-F]'
octit         : str = r'[0-7]'
digit         : str = r'[0-9]'
alpha         : str = r'[_a-zA-Z]'
asr_alpha_mer : str = r'[_a-zA-Z0-9@~]'


# Really want Pattern[str] and re.compile


# Issue #1946


# hex_pat : str = fr'-?0[xX]{hexit}+'
# oct_pat : str = fr'-?0{octit}+'
# int_pat : str = fr'-?{digit}+'
# dec_pat : str = fr'(-?{digit})M'
# # Not kosher Clojure
# sym_pat : str = fr'({alpha}{asr_alpha_mer}*)'


# Manual substitution as a workaround to Issue #1946


hex_pat : str = r'-?0[xX][0-9a-fA-F]+'
oct_pat : str = r'-?0o[0-7]+'
int_pat : str = r'-?[0-9]+'
dec_pat : str = r'(-?[0-9])M'
# Not kosher Clojure
sym_pat : str = r'([_a-zA-Z][_a-zA-Z0-9@~]*)'


# Multiplicity = str
ONE_OR_ZERO  : str = "?"
ONE_OR_MORE  : str = "+"
ZERO_OR_MORE : str = "*"
EXACT        : str = "X"
RANGE        : str = "R"


@dataclass
class ReRange:
    start_char_ord : i32
    end_char_ord   : i32


def check_re_range(self : ReRange, char : str) -> bool:
    o : i32 = ord(char)
    result : bool = (o >= self.start_char_ord) and \
                    (o <= self.end_char_ord)
    return result


def check_valid_ReRange(rr : ReRange):
    assert (rr.start_char_ord <= rr.end_char_ord)


def check_re_range_alternatives(
        alts : list[ReRange],
        char : str) -> bool:
    # Issue 1994
    # result : bool = False
    # if len(alts) == 0:
    #     return result
    # rr : ReRange = alts[0]
    # for rr in alts:
    #     if check_re_range(rr, char):
    #         result = True
    #         break
    # return result

    if len(alts) == 0:
        return False
    index : i32 = 0
    rr : ReRange = alts[index]
    # check_valid_ReRange(rr)
    while True:
        if check_re_range(rr, char):
            return True
        index += 1
        if index == len(alts):
            return False
        else:
            rr = alts[index]
            # check_valid_ReRange(rr)


lower_case_alpha_range : ReRange = ReRange(ord('a'), ord('z'))
upper_case_alpha_range : ReRange = ReRange(ord('A'), ord('Z'))

underscore             : ReRange = ReRange(ord('_'), ord('_'))
special_AT             : ReRange = ReRange(ord('@'), ord('@'))
special_TILDE          : ReRange = ReRange(ord('~'), ord('~'))

sym_first_pattern : list[ReRange] = \
    [underscore, lower_case_alpha_range, upper_case_alpha_range]

digit_range            : ReRange = ReRange(ord('0'), ord('9'))

# Issue #1992
# sym_rest_pattern  : list[ReRange] = \
#     sym_first_pattern + [special_AT, special_TILDE]
sym_rest_pattern : list[ReRange] = \
    [underscore, lower_case_alpha_range, digit_range,
     upper_case_alpha_range, special_AT, special_TILDE]

digit_pattern : list[ReRange] = [digit_range, underscore]
octit_range            : ReRange = ReRange(ord('0'), ord('7'))
octit_pattern : list[ReRange] = [octit_range, underscore]
hex_af                 : ReRange = ReRange(ord('a'), ord('f'))
hex_AF                 : ReRange = ReRange(ord('A'), ord('F'))
hexit_pattern : list[ReRange] = [digit_range,
                                 hex_af, hex_AF,
                                 underscore]
bit_range              : ReRange = ReRange(ord('0'), ord('1'))
bit_pattern   : list[ReRange] = [bit_range, underscore]


# Issue2003
# hexit_pattern : list[ReRange] = [digit_range,
#                                  ReRange(ord('a'), ord('f')),
#                                  ReRange(ord('A'), ord('F'))]


def match_symbol(candidate : str) -> bool:
    """In lieu of a table-driven regex compiler, which
    would be cool but considerable work, perhaps not
    justified if we can call into CPython libraries."""
    if candidate == '':
        return False
    if not check_re_range_alternatives(
            sym_first_pattern, candidate[0]):
        return False
    c : str  # implement Kleene *
    for c in candidate[1:]:
        if not check_re_range_alternatives(sym_rest_pattern, c):
            return False
    return True
    # Issue 2001


def match_integer(candidate : str) -> bool:
    """In lieu of a table-driven regex compiler, which
    would be cool but considerable work, perhaps not
    justified if we can call into CPython libraries."""
    # Issue 2006 -- attempt to reduce boilerplate not so good.
    # def check_syntax(c : str, last : str, i : i32, mxx : i32):
    #     pass
    if candidate == '':
        return False
    c : str
    last : str = ''  # exclude internal double __ and exclude trailing _
    mac : i32 = len(candidate)
    mxx : i32 = mac - 1
    if candidate[0] == '0':
        if mac == 1:
            return True
        assert mac >= 2
        i : i32 = 2
        # 000 == 0; leading 0 is allowed for 0 only (?)
        # 0_00 == 0 also
        if (candidate[1] == '0'):
            for c in candidate[2:]:
                if (c != '0') and (c != '_'):
                    return False
                check_numerical_syntax(c, last, i, mxx)
                i += 1
                last = c
        elif (candidate[1] == 'o') or (candidate[1] == 'O'):
            check_radical_len(candidate)
            for c in candidate[2:]:
                check_numerical_syntax(c, last, i, mxx)
                if not check_re_range_alternatives(octit_pattern, c):
                    return False
                i += 1
                last = c
        elif (candidate[1] == 'x') or (candidate[1] == 'X'):
            check_radical_len(candidate)
            for c in candidate[2:]:
                check_numerical_syntax(c, last, i, mxx)
                if not check_re_range_alternatives(hexit_pattern, c):
                    return False
                i += 1
                last = c
        elif (candidate[1] == 'b') or (candidate[1] == 'B'):
            check_radical_len(candidate)
            for c in candidate[2:]:
                check_numerical_syntax(c, last, i, mxx)
                if not check_re_range_alternatives(bit_pattern, c):
                    return False
                i += 1
                last = c
        else:
            raise SyntaxError
        return True
    elif candidate[0] == "_":
        return False
    else:  # leading is not zero
        i = 0
        for c in candidate:
            check_numerical_syntax(c, last, i, mxx)
            if not check_re_range_alternatives(digit_pattern, c):
                return False
        return True


def check_radical_len(candidate : str):
    if len(candidate[2:]) < 1:
        raise SyntaxError


def check_numerical_syntax(c:str, last:str, i:i32, mxx:i32):
    if (c == '_') and ((last == '_') or (i == mxx)):
        raise SyntaxError


NUMERICAL_NOISE : list[str] = ['o', 'O', 'b', 'B', 'x', 'X']


def strip_numerical_noise(s : str) -> str:
    """Assume input has been through 'match_integer'."""
    result : str = ''
    i : i32 = 0
    if s[0] == '0':
        if len(s) > 1 and in_(s[1], NUMERICAL_NOISE):
            i = 2
    j : i32
    for j in range(i, len(s)):
        if s[j] != '_':
            result += s[j]
    return result


I4C: dict[str, i32] = {
    '0': 0, '1': 1, '2': 2, '3': 3,
    '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9,
    'a': 10, 'b': 11, 'c': 12, 'd': 13,
    'A': 10, 'B': 11, 'C': 12, 'D': 13,
    'e': 14, 'f': 15,
    'E': 14, 'F': 15}


def cnvi(s : str, base : i32=10) -> i32:
    """Assume input has been through 'match_integer'."""
    assert base == 10 or base == 8 or base == 16 or base == 2
    result : i32 = 0
    c : str
    t : str = strip_numerical_noise(s)
    pow: i32 = base ** (len(t) - 1)
    for c in t:
        incr : i32 = pow * I4C[c]
        result += incr
        # pow //= base
        pow = (pow // base)
    return result


#   ___                    _____       _
#  | _ \___ __ _ _____ __ |_   _|__ __| |_
#  |   / -_) _` / -_) \ /   | |/ -_|_-<  _|
#  |_|_\___\__, \___/_\_\   |_|\___/__/\__|
#          |___/


def regex_test() -> None:
    print('REGEX TEST')
    assert ord('a') >= ord('a')
    assert ord('a') <= ord('z')

    rr : ReRange = ReRange(ord('a'), ord('z'))
    assert check_re_range(rr, 'x')
    assert not check_re_range(rr, '@')

    assert check_re_range_alternatives(sym_first_pattern, '_')
    assert check_re_range_alternatives(sym_rest_pattern,  '_')
    assert check_re_range_alternatives(sym_rest_pattern,  '9')
    assert check_re_range_alternatives(sym_rest_pattern,  '~')
    assert not check_re_range_alternatives(sym_rest_pattern,  ':')

    assert match_symbol('Integer')
    assert match_symbol('_foobar')
    assert match_symbol('_foobar__lpython_global__42_')
    assert match_symbol('_foobar__@lpython_global_~WEIRD__42_')
    assert not match_symbol(':clojure-keyword')
    assert not match_symbol('::clojure-qualified-keyword')
    assert not match_symbol('asr_keyword:')
    assert not match_symbol('4')
    assert not match_symbol('')
    assert not match_symbol('[')
    assert not match_symbol('foo bar')

    assert match_integer('00')
    assert match_integer('4')
    assert not match_integer('_42')
    assert match_symbol('_42')
    assert match_integer('42_0')
    assert match_integer('0xBADBEEF')
    assert match_integer('0x_BAD_BEEF')
    # we don't have try-except, so these expected throws are commented
    # assert not match_integer('0x')
    # assert not match_integer('0o')
    # match_integer('0x_BAD__BEEF')  # Expected SyntaxError!
    # match_integer('0x_BAD_BEEF_')  # Expected SyntaxError!
    assert not match_integer('0x@#$%')
    assert match_integer('0b101010')
    assert match_integer('0B1111_0100_111')

    assert cnvi('0b0', base=2) == 0
    assert cnvi('0b1', base=2) == 1
    assert cnvi('0b10', base=2) == 2
    assert cnvi('0b11', base=2) == 3
    assert cnvi('0b1111_0100_111', base=2) == 1959
    assert cnvi("0x7a7", base=16) == 1959
    assert cnvi("0o3647", base=8) == 1959

    # assert cnvi('0B1111_0100_111', base=2) == 1959

    # assert match_integer('0b101010')

    # Issue 2004: nullptr!
    # Issue 2007: heisenbug!
    # assert i32('1959', base=10) == 1959
    # assert i32('0b101010', base=2) == 42

    # try-except not implemented
    # assert not match_integer('0Y1234')

    assert 000 == 0
    assert 0_000 == 0

    # Issue 2002 -- should be syntax errors
    # assert 07 == 7
    # assert 08 == 8
    assert hex(1959) == '0x7a7'
    assert oct(1959) == '0o3647'
    assert i32(1959) == 1959
    assert i32(1_959) == 1_959

    # Issue 2004 -- doesn't work in CPython
    # assert i32('0x7a7', base=16) == 1959
    # assert i32('1959', base=10) == 1959

    # assert i32('1959', base=10) == 1959

    # Issue 2004 -- doesn't work in LPython
    # assert i32('1959') == 1959 # Issue 2004

    # Issue 2004 -- doesn't work in CPython
    # assert i32(hex(1959), base=16) == 1959

    # Issue 2004 -- doesn't work in CPython
    # assert i32(oct(1959), base=8) == 1959

    assert 42_0 == 420  # NICE!
    _42 : i32 = 0  # if uninitialized, MIGHT be == 42 !
    assert not _42  == 42


#  _
# | |   _____ _____ _ _
# | |__/ -_) \ / -_) '_|
# |____\___/_\_\___|_|


INT_TT : str = "integer"
FLT_TT : str = "float"
SYM_TT : str = "asr improper symbol"
PNC_TT : str = "punctuation"
MCR_TT : str = "reader macro"
NKW_TT : str = "non-qualified keyword"
QKW_TT : str = "qualified keyword"
AKW_TT : str = "asr improper keyword"


# Line    : Any = i32
# Col     : Any = i32
# LTType  : Any = Optional[str]
# LTVal   : Any = Optional[Union[str, i32]]
# LTTuple : Any = Tuple[Line, Col, LTType, LTVal]


# Issue 1954

@dataclass
class LasrLexer:
    fd   : StringIO = StringIO('', 0, 0) # prefer Optional[StringIO]
    line : i32 = 1 # prefer Line
    col  : i32 = 1 # prefer Col
    type : str = '' # prefer LTType
    val  : str = '' # prefer LTVal


def back1(self : LasrLexer) -> i32:
    result: i32 = seek(self.fd, tell(self.fd) - 1, SEEK_SET)
    return result


def peek(self : LasrLexer) -> str:
    result : str = read(self.fd, 1)
    if result != EOF_SIGNAL:
        back1(self)
    return result


def in_(c: str, l: list[str]) -> bool:
    result : bool = False
    s : str
    for s in l:
        if s == c:
            result = True
            break
    return result


def eat_white(self : InOut[LasrLexer]) -> None:
    c : str = peek_debug(self)
    while c != EOF_SIGNAL and in_(c, WHITESPACE):
        if c == NEWLINE:
            self.col = 1
            self.line += 1
            c = read(self.fd, 1)
            assert c == NEWLINE
        else:
            self.col += 1
            c = read(self.fd, 1)
            assert in_(c, WHITESPACE)
        c = peek_debug(self)


def get_non_white(self : InOut[LasrLexer]) -> tuple[i32, str]:
    string : str = ''
    eat_white(self)
    col_before : i32 = self.col
    c: str = read(self.fd, 1)
    self.col += 1
    while c != EOF_SIGNAL and not in_(c, WHITESPACE):
        string += c
        if in_(c, RDR_MACROS):
            break
        if in_(c, COLL_OPENERS) or in_(c, COLL_CLOSERS):
            break
        c = read(self.fd, 1)
        self.col += 1
    if in_(c, WHITESPACE):
        back1(self)
        self.col -= 1
    elif c == EOF_SIGNAL:
        self.col = self.fd._len + 1
    return col_before, string


@dataclass
class Token:
    line       : i32
    col_before : i32
    col_after  : i32
    lttype     : str
    ltval      : str


# Because I don't have Optional[LTType] and Optional[LTVal]
NO_TOKEN_TYPE  : str = ''
NO_TOKEN_VALUE : str = ''


def next(self : InOut[LasrLexer]) -> Token :
    result : Token = Token(
        -1, -1, -1, NO_TOKEN_TYPE, NO_TOKEN_VALUE)
    c : i32 = 0
    s : str = ''
    c, s = get_non_white(self)
    if match_integer(s):
        result = Token(self.line, c, self.col, INT_TT, s)
    elif match_symbol(s):
        result = Token(self.line, c, self.col, SYM_TT, s)
    elif in_(s, COLL_OPENERS) or in_(s, COLL_CLOSERS):
        result = Token(self.line, c, self.col, PNC_TT, s)
    return result


def peek_debug(self : InOut[LasrLexer]) -> str:
    dump : bool = False
    if dump:
        print('self.fd._len = ', end='')
        print(self.fd._len, end='')
        print('.')
        print('self.fd._0cursor = ', end='')
        print(self.fd._0cursor, end='')
        print('.')
    c: str = peek(self)
    if dump:
        print('eat-white line 175, c = "', end='')
        print(c, end='')
        print('".')
        print('self.fd._len = ', end='')
        print(self.fd._len, end='')
        print('.')
        print('self.fd._0cursor = ', end='')
        print(self.fd._0cursor, end='')
        print('.')
    return c


def lex_str(input_str: str) -> list[Token]:
    lexer : LasrLexer = LasrLexer(StringIO(input_str))
    __post_init__(lexer.fd)
    result : list[Token] = []
    tok : Token = next(lexer)
    while tok.ltval != NO_TOKEN_VALUE:
        result.append(tok)
        tok = next(lexer)
    return result


#   _                      _____       _
#  | |   _____ _____ _ _  |_   _|__ __| |_
#  | |__/ -_) \ / -_) '_|   | |/ -_|_-<  _|
#  |____\___/_\_\___|_|     |_|\___/__/\__|


def lexer_test() -> None: # lexer : InOut[LasrLexer]):
    # Issue #1981
    print('LEXER TEST')
    first_lexer_test()
    second_lexer_test()
    third_lexer_test()
    fourth_lexer_test()


def fourth_lexer_test():
    lts: list[Token] = lex_str('(Integer 4 [])')
    assert lts == [
        Token(1,  1,  2, PNC_TT, "("),
        Token(1,  2,  9, SYM_TT, "Integer"),
        Token(1, 10, 11, INT_TT, "4"),
        Token(1, 12, 13, PNC_TT, "["),
        Token(1, 13, 14, PNC_TT, "]"),
        Token(1, 14, 15, PNC_TT, ")"),
        ]


def third_lexer_test():
    lexer : LasrLexer = LasrLexer(StringIO('(Integer 4 [])'))
    __post_init__(lexer.fd)
    # Col is left AFTER the token.
    token: Token = next(lexer)
    assert token.line == 1
    assert token.col_after == 2
    assert token.col_before == 1
    assert token.lttype == PNC_TT
    assert token.ltval == '('
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 9
    assert token.col_before == 2
    assert token.lttype == SYM_TT
    assert token.ltval == 'Integer'
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 11
    assert token.col_before == 10
    assert token.lttype == INT_TT
    assert token.ltval == '4'
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 13
    assert token.col_before == 12
    assert token.lttype == PNC_TT
    assert token.ltval == '['
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 14
    assert token.col_before == 13
    assert token.lttype == PNC_TT
    assert token.ltval == ']'
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 15
    assert token.col_before == 14
    assert token.lttype == PNC_TT
    assert token.ltval == ')'
    token = next(lexer)
    assert token.line == -1
    assert token.col_after == -1
    assert token.col_before == -1
    assert token.lttype == NO_TOKEN_TYPE
    assert token.ltval == NO_TOKEN_VALUE
    lexer = LasrLexer(StringIO('    foo\n  42\n'))
    __post_init__(lexer.fd)
    token = next(lexer)
    assert token.line == 1
    assert token.col_after == 8
    assert token.col_before == 5
    assert token.lttype == SYM_TT
    assert token.ltval == 'foo'
    token = next(lexer)
    assert token.line == 2
    assert token.col_after == 5
    assert token.col_before == 3
    assert token.lttype == INT_TT
    assert token.ltval == '42'
    token = next(lexer)
    assert token.line == -1
    assert token.col_after == -1
    assert token.col_before == -1
    assert token.lttype == NO_TOKEN_TYPE
    assert token.ltval == NO_TOKEN_VALUE


def second_lexer_test():
    lexer : LasrLexer = LasrLexer(StringIO('(Integer 4 [])'))
    __post_init__(lexer.fd)
    check_integer_ttype(lexer)
    # repeatability
    seek(lexer.fd, 0, SEEK_SET)
    lexer.col = 1  # don't forget !
    check_integer_ttype(lexer)


def first_lexer_test():
    lexer : LasrLexer = LasrLexer(StringIO('  foo  bar  '))
    __post_init__(lexer.fd)
    eat_white(lexer)
    t : str = peek_debug(lexer)
    # Issue 1971 print({"t": t})
    assert t == 'f', "t == 'f'"


def check_integer_ttype(lexer : InOut[LasrLexer]):
    """Not really a parse."""
    c : i32
    t : str
    c, t = get_non_white(lexer)
    assert t == '(', "t = '('"
    assert c == 1
    assert lexer.col == 2
    c, t = get_non_white(lexer)
    assert t == 'Integer', "t = 'Integer'"
    assert c == 2
    assert lexer.col == 9
    c, t = get_non_white(lexer)
    assert t == '4'
    assert c == 10
    assert lexer.col == 11
    c, t = get_non_white(lexer)
    assert t == '['
    assert c == 12
    assert lexer.col == 13
    c, t = get_non_white(lexer)
    assert c == 13
    assert t == ']'
    assert lexer.col == 14
    c, t = get_non_white(lexer)
    assert c == 14
    assert t == ')'
    assert lexer.col == 15
    # idempotency of EOF
    _: i32
    for _ in range(10):
        c, t = get_non_white(lexer)
        assert t == EOF_SIGNAL
        assert c == 15  # cool!
        assert lexer.col == 15


# Issue 2033 can't refactor tests into their own files.


#  ___
# | _ \__ _ _ _ ___ ___ _ _
# |  _/ _` | '_(_-</ -_) '_|
# |_| \__,_|_| /__/\___|_|


#
# This is an independent implementation of ASR.
# It does aggressive type-checking and conversions.
#
#
# I could have decided to make LASR depend on the
# Python script that generates C++ code from
# ASDL, but that would defeat the purpose of an
# independent implementation.
#
#
# lasr_parser is an old-fashioned, hand-written,
# recursive descent parser. No apologies for that.
#


# Issue 1943
# LPython doesn't have type aliases, yet.
# FullForm = dict[str, dict[str, Any]]


#   _  _         _       _____
#  | \| |___  __| |___  |_   _|  _ _ __  ___ ___
#  | .` / _ \/ _` / -_)   | || || | '_ \/ -_|_-<
#  |_|\_\___/\__,_\___|   |_| \_, | .__/\___/__/
#                             |__/|_|
#
# Corresponding to "terms" in the ASDL for ASR,
# on the left-hand sides of equals signs.


TTYPE_TERM : str = "ttype"


#     _   _ _                     _   _
#    /_\ | | |_ ___ _ _ _ _  __ _| |_(_)_ _____ ___
#   / _ \| |  _/ -_) '_| ' \/ _` |  _| \ V / -_|_-<
#  /_/ \_\_|\__\___|_| |_||_\__,_|\__|_|\_/\___/__/
#
# Corresponding to "heads" in the ASDL for ASR,
# on the right-hand sides of equals signs.


INTEGER_TTYPE   : str = "Integer"
LOGICAL_TTYPE   : str = "Logical"
REAL_TTYPE      : str = "Real"
COMPLEX_TTYPE   : str = "Complex"
STRING_TTYPE    : str = "String"


# Issue 2024: set types not supported

# INTEGER_KINDS   : set[i32] = {1, 2, 4, 8}
# LOGICAL_KINDS   : set[i32] = {1, 2, 4}
# REAL_KINDS      : set[i32] = {4, 8}
# COMPLEX_KINDS   : set[i32] = {4, 8}
# CHARACTER_KINDS : set[i32] = {1}

# Undesirable workaround:

INTEGER_KINDS   : dict[i32, i32] = {1: 1, 2: 2, 4: 4, 8: 8}
LOGICAL_KINDS   : dict[i32, i32] = {1: 1, 2: 2, 4: 4}
REAL_KINDS      : dict[i32, i32] = {4: 4, 8: 8}
COMPLEX_KINDS   : dict[i32, i32] = {4: 4, 8: 8}
CHARACTER_KINDS : dict[i32, i32] = {1: 1}


#   ___            _                   _        _   _
#  |_ _|_ __  _ __| |___ _ __  ___ _ _| |_ __ _| |_(_)___ _ _  ___
#   | || '  \| '_ \ / -_) '  \/ -_) ' \  _/ _` |  _| / _ \ ' \(_-<
#  |___|_|_|_| .__/_\___|_|_|_\___|_||_\__\__,_|\__|_\___/_||_/__/
#            |_|


@dataclass
class Node:
    lexer : LasrLexer = LasrLexer()
    line  : i32 = 0
    col   : i32 = 0


def must_be(self : InOut[Node], v: str) -> bool:
    token : Token = next(self.lexer)
    self.line = token.line
    self.col  = token.col_before
    if v != token.ltval:
        print('Syntax error on line ' , end='')
        print(token.line              , end='')
        print(', column '             , end='')
        print(token.col_before        , end='')
        print('.')
        print('Token value must be '  , end='')
        print(v                       , end='')
        print(', not '                , end='')
        print(token.ltval             , end='')
        print('.')
        # print(f'Syntax error on line {token.line}, column {token.col_before}')
        # print(f'Token Value must be {v}, not {token.ltval}')
        return False
    return True


def get_of_type(self: InOut[Node], tt: str) -> str:
    token : Token = next(self.lexer)
    self.line = token.line
    self.col  = token.col_before
    if tt != token.lttype:
        print('Syntax error on line ' , end='')
        print(token.line              , end='')
        print(', column '             , end='')
        print(token.col_before        , end='')
        print('.')
        print('Token type must be '   , end='')
        print(tt                      , end='')
        print(', not '                , end='')
        print(token.lttype            , end='')
        print('.')
        # print(f'Syntax error on line {token.line_1}, column {token.col_start_1}')
        # print(f'Token Type must be {tt}, not {token.type}')
        return NO_TOKEN_TYPE
    return token.ltval


MULTIPLICITY_ZERO_OR_MORE : str = "*"
MULTIPLICITY_ONE_OR_MORE  : str = "+"
MULTIPLICITY_ZERO_OR_ONE  : str = "?"
MULTIPLICITY_EXACTLY_ONCE : str = ""


@dataclass
class MultiplicityNode: # (Node)
    node         : Node = Node()
    # Model inheritance by containment.
    multiplicity : str  = '' # Issue 2030 MULTIPLICITY_EXACTLY_ONCE
    emptyQ       : bool = True


@dataclass
class Dimensions: # (MultiplicityNode)
    """This is not a term node in ASR. It's a multiplicity."""
    contents : list[i32]
    multi    : MultiplicityNode = MultiplicityNode ()
    # Model inheritance by containment.


NO_CONTENTS : list[i32] = []
DEAD_LIST   : list[i32] = [-1]

#   ___                        _____       _
#  | _ \__ _ _ _ ___ ___ _ _  |_   _|__ __| |_
#  |  _/ _` | '_(_-</ -_) '_|   | |/ -_|_-<  _|
#  |_| \__,_|_| /__/\___|_|     |_|\___/__/\__|


def parser_test():
    dims : Dimensions = \
        Dimensions(
            multi=MultiplicityNode(
                node=Node(
                    lexer=LasrLexer(StringIO(
                        '(Integer 4 [])')),
                    line=0,
                    col=0),
                multiplicity=MULTIPLICITY_ZERO_OR_MORE,
                emptyQ=True),
            contents=DEAD_LIST
        )
    __post_init__(dims.multi.node.lexer.fd)
    # Issue 2044
    print(dims.multi.node.lexer.fd)
    must_be(dims.multi.node, LIST_OPEN)
    victim : str = get_of_type(dims.multi.node, SYM_TT)
    assert victim == "Integer"
    victim = get_of_type(dims.multi.node, INT_TT)
    assert victim == '4'
    must_be(dims.multi.node, VECT_OPEN)
    must_be(dims.multi.node, VECT_CLOSE)
    must_be(dims.multi.node, LIST_CLOSE)


#  __  __      _
# |  \/  |__ _(_)_ _
# | |\/| / _` | | ' \
# |_|  |_\__,_|_|_||_|


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'

    fd   : StringIO = StringIO(integer_asr)
    __post_init__(fd)  # Issue #1929

    stringio_test(fd, integer_asr)
    regex_test()
    lexer_test() # lexer)
    parser_test()

    # hdc_test()


# from typing import Union, Optional, List, Tuple


# #   ___                   _        _    _
# #  | __|_ ___ __  ___ _ _| |_ __ _| |__| |___
# #  | _|\ \ / '_ \/ _ \ '_|  _/ _` | '_ \ / -_)
# #  |___/_\_\ .__/\___/_|  \__\__,_|_.__/_\___|
# #          |_|


# INT_TT : str = "int"
# FLT_TT : str = "float"
# SYM_TT : str = "asr improper symbol"
# PNC_TT : str = "punctuation"
# MCR_TT : str = "reader macro"
# NKW_TT : str = "non-qualified keyword"
# QKW_TT : str = "qualified keyword"
# AKW_TT : str = "asr improper keyword"


# Line    = int
# Col     = int
# LTType  = Optional[str]
# LTVal   = Optional[Union[str, int]]
# LTTuple = Tuple[Line, Col, LTType, LTVal]


# #   ___     _                     _
# #  |_ _|_ _| |_ ___ _ _ _ _  __ _| |
# #   | || ' \  _/ -_) '_| ' \/ _` | |
# #  |___|_||_\__\___|_| |_||_\__,_|_|


# NEWLINE      : str       = "\n"
# WHITESPACE   : List[str] = [" ", ",", NEWLINE, "\r", "\t"]
# RDR_MACROS   : List[str] = ["#_", "#'", "#:"]


# LIST_OPEN    : str       = "("
# VECT_OPEN    : str       = "["
# HMAP_OPEN    : str       = "{"
# HSET_OPEN    : str       = "#{"
# COLL_OPENERS : List[str] = [LIST_OPEN, VECT_OPEN,
#                             HMAP_OPEN, HSET_OPEN]

# LIST_CLOSE   : str       = ")"
# VECT_CLOSE   : str       = "]"
# HASH_CLOSE   : str       = "}"  # for both HMAP & HSET
# COLL_CLOSERS : List[str] = [LIST_CLOSE, VECT_CLOSE, HASH_CLOSE]

# EOF_SIGNAL   : str       = ''
