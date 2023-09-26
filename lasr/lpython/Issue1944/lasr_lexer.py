# from dataclasses import dataclass
# i32 = int
# from typing import \
#     Generic, TypeVar, Optional, Union, \
#     Tuple, Any, List, Pattern
# T_ = TypeVar('T_')
# class InOut(Generic[T_]):
#     pass


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
    _0cursor : i32 = i32(0)
    _len     : i32 = i32(0)


# Issue #1930: InOut type


def __post_init__(this: InOut[StringIO]):
    """Should be a member method of 'StringIO'."""
    """Imitate the behavior of Python 3.10.2 io library."""
    this._len = len(this._buf)


def tell(this: InOut[StringIO]) -> i32:
    """Should be a member method of 'StringIO'."""
    """Imitate the behavior of Python 3.10.2 io library."""
    result : i32 = this._0cursor
    return result


def read(this: InOut[StringIO], chars : i32) -> str:
    """Should be a member method of 'StringIO'."""
    """Imitate the behavior of Python 3.10.2 io library."""
    """On any negative number, read from cursor to end."""
    result : str = ''  # EOF
    if chars < 0:
        result = this._buf[this._0cursor : this._len]
        this._0cursor = this._len
    else:
        mac: i32 = min(this._len, this._0cursor + chars)
        assert mac <= this._len  # check 'min'
        result = this._buf[this._0cursor : mac]
        # Python 3.10.2 is observed NOT to reset cursor to 'mac'
        # if cursor is > mac! Subsequent tells will report a
        # value that is too large!
        if mac < this._len:
            this._0cursor = mac
    return result


# Issue #1939: 'Literal' type hint


SEEK_SET : i32 = 0
SEEK_CUR : i32 = 1
SEEK_END : i32 = 2


def seek(this: InOut[StringIO], offset: i32, whence : i32) -> i32:
    """Imitate the behavior of Python 3.10.2 io library."""
    pos : i32 = 0
    if whence == SEEK_SET:
        pos = offset
    elif whence == SEEK_CUR:
        pos = this._0cursor + offset
    elif whence == SEEK_END:
        pos = this._len + offset
    else:
        raise ValueError(f"""Invalid whence ({whence}, should be 0, 1, or 2""")
    if (pos < 0):
        raise ValueError(f"""Negative seek position {pos}""")
    # Python 3.10.2 permits seeking beyond the end of the file!
    this._0cursor = pos
    return pos


#  ___ _       _           ___ ___    _          _
# / __| |_ _ _(_)_ _  __ _|_ _/ _ \  | |_ ___ __| |_
# \__ \  _| '_| | ' \/ _` || | (_) | |  _/ -_|_-<  _|
# |___/\__|_| |_|_||_\__, |___\___/   \__\___/__/\__|
#                    |___/


def stringio_test(fd : InOut[StringIO], integer_asr : str):
    assert fd._buf == integer_asr
    assert fd._len == len(integer_asr)


def read_seek_tell_test(fd : InOut[StringIO]):
    a_char: str = read(fd, 1)
    assert a_char == '('
    a_char = read(fd, 1)
    assert a_char == 'I'
    assert tell(fd) == 2
    assert seek(fd, 0, SEEK_SET) == 0
    assert seek(fd, 100, SEEK_SET) == 100
    assert seek(fd, 2, SEEK_SET) == 2
    temp: str = read(fd, -1)
    assert temp == 'nteger 4 [])'
    assert tell(fd) == 14


#  _ _ ___ __ _ _____ __
# | '_/ -_) _` / -_) \ /
# |_| \___\__, \___/_\_\
#         |___/


NEWLINE      : str       = "\n"
WHITESPACE   : List[str] = [" ", ",", NEWLINE, "\r", "\t"]
RDR_MACROS   : List[str] = ["#_", "#'", "#:"]


LIST_OPEN    : str       = "("
VECT_OPEN    : str       = "["
HMAP_OPEN    : str       = "{"
HSET_OPEN    : str       = "#{"
COLL_OPENERS : List[str] = [LIST_OPEN, VECT_OPEN,
                            HMAP_OPEN, HSET_OPEN]

LIST_CLOSE   : str       = ")"
VECT_CLOSE   : str       = "]"
HASH_CLOSE   : str       = "}"  # for both HMAP & HSET
COLL_CLOSERS : List[str] = [LIST_CLOSE, VECT_CLOSE, HASH_CLOSE]

EOF_SIGNAL   : str       = ''


hexit         : str = r'[0-9a-fA-F]'
octit         : str = r'[0-7]'
digit         : str = r'[0-9]'
alpha         : str = r'[_a-zA-Z]'
asr_alpha_mer : str = r'[_a-zA-Z0-9@~]'


hex_pat : Pattern[str] = fr'-?0[xX]{hexit}+'
oct_pat : Pattern[str] = fr'-?0{octit}+'
int_pat : Pattern[str] = fr'-?{digit}+'
dec_pat : Pattern[str] = fr'(-?{digit})M'
# Not kosher Clojure
sym_pat : Pattern[str] = fr'({alpha}{asr_alpha_mer}*)'




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


#             _
#  _ __  __ _(_)_ _
# | '  \/ _` | | ' \
# |_|_|_\__,_|_|_||_|


if __name__ == '__main__':
    integer_asr : str = '(Integer 4 [])'
    fd   : StringIO = StringIO(integer_asr, 0, 0)
    __post_init__(fd)  # Issue #1929
    stringio_test(fd, integer_asr)
    read_seek_tell_test(fd)


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
