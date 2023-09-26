from lpython import (dataclass, InOut, i32,
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


def stringio_test(fd : InOut[StringIO], integer_asr : str):
    print('STRINGIO TEST')
    assert fd._buf == integer_asr, "fd._buf == integer_asr"
    assert fd._len == len(integer_asr), "fd._len == len(integer_asr)"
    read_seek_tell_test(fd)


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


#  _ _ ___ __ _ _____ __
# | '_/ -_) _` / -_) \ /
# |_| \___\__, \___/_\_\
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
    # Issue 2001 ...


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



def strip_numerical_noise(s : str) -> str:
    result : str = ''
    # if s[0] == '0':
    #     if len(s) > 1 and
    return result


def cnvi(s : str, base : i32=10) -> i32:
    result : i32 = 0
    return result


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
# | |_____ _____ _ _
# | / -_) \ / -_) '_|
# |_\___/_\_\___|_|


INT_TT : str = "int"
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
        c = read(self.fd, 1)
        if c == NEWLINE:
            self.col = 1
            self.line += 1
        else:
            self.col += 1
        c = peek_debug(self)


def get_non_white(self : InOut[LasrLexer]) -> str:
    result : str = ""
    eat_white(self)
    c: str = read(self.fd, 1)
    while c != EOF_SIGNAL and not in_(c, WHITESPACE):
        result += c
        if in_(c, RDR_MACROS):
            break
        if in_(c, COLL_OPENERS) or in_(c, COLL_CLOSERS):
            break
        c = read(self.fd, 1)
    if in_(c, WHITESPACE):
        back1(self)
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


def lexer_test() -> None: # lexer : InOut[LasrLexer]):
    # Issue #1981
    print('LEXER TEST')
    # re-use these variables multiple times
    lexer : LasrLexer = LasrLexer() # Issue #1991; dummy value
    t : str = '' # Issue #1991; dummy value

    # first test
    lexer = LasrLexer(StringIO('  foo  bar  '))
    __post_init__(lexer.fd)
    eat_white(lexer)
    t = peek_debug(lexer)
    # Issue 1971 print({"t": t})
    assert t == 'f', "t == 'f'"

    # second test
    lexer = LasrLexer(StringIO('(Integer 4 [])'))
    __post_init__(lexer.fd)
    check_integer_ttype(lexer)
    # repeatability
    seek(lexer.fd, 0, SEEK_SET)
    check_integer_ttype(lexer)


def check_integer_ttype(lexer : InOut[LasrLexer]):
    t : str
    t = get_non_white(lexer)
    assert t == '(', "t = '('"
    t = get_non_white(lexer)
    assert t == 'Integer', "t = 'Integer'"
    t = get_non_white(lexer)
    assert t == '4'
    t = get_non_white(lexer)
    assert t == '['
    t = get_non_white(lexer)
    assert t == ']'
    t = get_non_white(lexer)
    assert t == ')'
    # idempotency of EOF
    _: i32
    for _ in range(10):
        t = get_non_white(lexer)
        assert t == EOF_SIGNAL


#             _
#  _ __  __ _(_)_ _
# | '  \/ _` | | ' \
# |_|_|_\__,_|_|_||_|


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'

    fd   : StringIO = StringIO(integer_asr)
    __post_init__(fd)  # Issue #1929

    stringio_test(fd, integer_asr)
    lexer_test() # lexer)
    regex_test()


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


# hexit         : str = r'[0-9a-fA-F]'
# octit         : str = r'[0-7]'
# digit         : str = r'[0-9]'
# alpha         : str = r'[_a-zA-Z]'
# asr_alpha_mer : str = r'[_a-zA-Z0-9@~]'


# hex_pat = re.compile(fr'-?0[xX]{hexit}+')
# oct_pat = re.compile(fr'-?0{octit}+')
# int_pat = re.compile(fr'-?{digit}+')
# dec_pat = re.compile(fr'(-?{digit})M')
# sym_pat = re.compile(fr'({alpha}{asr_alpha_mer}*)')  # Not kosher Clojure

#     # TODO: Consider re-implementing with BufferedIO

#     def _cons_res(self, tt : LTType, v : LTVal) -> LTTuple:
#         result: LTTuple = self.line, self.col, tt, v
#         return result

#     def next(self) -> LTTuple:
#         s : str = self.get_non_white()
#         if m := re.match(int_pat, s):
#             result = self._cons_res(INT_TT, int(m.group(0)))
#             self.col += len(s)
#             return result
#         elif m := re.match(sym_pat, s):
#             result = self._cons_res(SYM_TT, m.group(0))
#             self.col += len(s)
#             return result
#         elif s in COLL_OPENERS or s in COLL_CLOSERS:
#             result = self._cons_res(PNC_TT, s)
#             self.col += len(s)
#             return result
#         return -1, -1, None, None


# def lex_str(input_str: str) -> List[LTTuple]:
#     tok : LasrLexer = LasrLexer(io.StringIO(input_str))
#     result : List[LTTuple] = []
#     line, col, tipe, val = tok.next()
#     while val is not None:
#         result.append((line, col, tipe, val))
#         line, col, tipe, val = tok.next()
#     return result
