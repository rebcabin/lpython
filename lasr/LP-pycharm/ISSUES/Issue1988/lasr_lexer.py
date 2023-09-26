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
oct_pat : str = r'-?0[0-7]+'
int_pat : str = r'-?[0-9]+'
dec_pat : str = r'(-?[0-9])M'
# Not kosher Clojure
sym_pat : str = r'([_a-zA-Z][_a-zA-Z0-9@~]*)'


@dataclass
class Match:
    group : list[str]


@dataclass
class Pattern:
    _foo : str
    pass


# def match(pat : str, string : str) -> Optional[list[str] | str]:
#     return None


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
        c = peek(self)


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
        print('self.fd._len = ', end='');
        print(self.fd._len, end='');
        print('.')
        print('self.fd._0cursor = ', end='');
        print(self.fd._0cursor, end='');
        print('.')
    c: str = peek(self)
    if dump:
        print('eat-white line 175, c = "', end='')
        print(c, end='');
        print('".')
        print('self.fd._len = ', end='');
        print(self.fd._len, end='');
        print('.')
        print('self.fd._0cursor = ', end='');
        print(self.fd._0cursor, end='');
        print('.')
    return c


def lexer_test() -> None: # lexer : InOut[LasrLexer]):
    # Issue #1981
    print('LEXER TEST')
    lexer : LasrLexer = LasrLexer(StringIO('  foo  bar  '))
    __post_init__(lexer.fd)

    eat_white(lexer)
    t : str = peek(lexer)
    # Issue 1971 print({"t": t})
    assert t == 'f', "t == 'f'"

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


# class LasrLexer:

#     def __init__(self, fd : io.IOBase):
#         self.fd   : io.IOBase   = fd
#         self.line : Line   = 1
#         self.col  : Col    = 1
#         self.type : LTType = None
#         self.val  : LTVal  = None

#     # TODO: Consider re-implementing with BufferedIO

#     def back1(self) -> int:
#         result: int = self.fd.seek(self.fd.tell() - 1, io.SEEK_SET)
#         return result

#     def peek(self) -> Union[str, None]:
#         result : str = self.fd.read(1)
#         if result != EOF_SIGNAL:
#             self.back1()
#         return result

#     def eat_white(self) -> None:
#         c : str = self.peek()
#         while c != EOF_SIGNAL and c in WHITESPACE:
#             c = self.fd.read(1)
#             if c == NEWLINE:
#                 self.col = 1
#                 self.line += 1
#             else:
#                 self.col += 1
#             c = self.peek()

#     def get_non_white(self) -> str:
#         result = ""
#         self.eat_white()
#         c : str = self.fd.read(1)
#         while c != EOF_SIGNAL and c not in WHITESPACE:
#             result += c
#             if c in RDR_MACROS:
#                 break
#             if c in COLL_OPENERS or c in COLL_CLOSERS:
#                 break
#             c = self.fd.read(1)
#         if c in WHITESPACE:
#             self.back1()
#         return result

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
