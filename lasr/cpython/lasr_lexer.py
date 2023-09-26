import re
print()
print("# ****************************************** #")
print(re.__file__)

import io
from dataclasses import dataclass
import decimal  # TODO big decimal


from typing import Union, Optional, List, Tuple, Pattern


#   ___                   _        _    _
#  | __|_ ___ __  ___ _ _| |_ __ _| |__| |___
#  | _|\ \ / '_ \/ _ \ '_|  _/ _` | '_ \ / -_)
#  |___/_\_\ .__/\___/_|  \__\__,_|_.__/_\___|
#          |_|


INT_TT : str = "int"
FLT_TT : str = "float"
SYM_TT : str = "asr improper symbol"
PNC_TT : str = "punctuation"
MCR_TT : str = "reader macro"
NKW_TT : str = "non-qualified keyword"
QKW_TT : str = "qualified keyword"
AKW_TT : str = "asr improper keyword"


Line        = int
Col         = int
LTType      = Optional[str]
LTVal       = Optional[Union[str, int]]


#   ___     _                     _
#  |_ _|_ _| |_ ___ _ _ _ _  __ _| |
#   | || ' \  _/ -_) '_| ' \/ _` | |
#  |___|_||_\__\___|_| |_||_\__,_|_|


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


hex_pat : Pattern[str] = re.compile(fr'-?0[xX]{hexit}+')
oct_pat : Pattern[str] = re.compile(fr'-?0{octit}+')
int_pat : Pattern[str] = re.compile(fr'-?{digit}+')
dec_pat : Pattern[str] = re.compile(fr'(-?{digit})M')
sym_pat : Pattern[str] = re.compile(fr'({alpha}{asr_alpha_mer}*)')  # Not kosher Clojure


@dataclass
class Token:
    line_1       : Line  # 1-based
    col_start_1  : Col   # START of the token (1-based)
    type         : LTType
    val          : LTVal


class LasrLexer:

    def __init__(self, fd : io.IOBase):
        self.fd                 : io.IOBase = fd
        self.line               : Line      = 1
        self.col_after_1_based  : Col       = 1
        self.type               : LTType    = None
        self.val                : LTVal     = None

    # TODO: Consider re-implementing with BufferedIO

    def back1(self) -> int:
        result: int = self.fd.seek(self.fd.tell() - 1, io.SEEK_SET)
        return result

    def peek(self) -> Union[str, None]:
        result : str = self.fd.read(1)
        if result != EOF_SIGNAL:
            self.back1()
        return result

    def eat_white(self) -> None:
        c : str = self.peek()
        while c != EOF_SIGNAL and c in WHITESPACE:
            if c == NEWLINE:
                self.col_after_1_based = 1
                self.line += 1
                c = self.fd.read(1)
                assert c == NEWLINE
            else:
                self.col_after_1_based += 1
                c = self.fd.read(1)
                assert c in WHITESPACE
            c = self.peek()

    def get_non_white(self) -> tuple[Col, str]:
        string : str = ""
        self.eat_white()
        start_col_1 : int = self.col_after_1_based
        c : str = self.fd.read(1)
        self.col_after_1_based += 1
        while c != EOF_SIGNAL and c not in WHITESPACE:
            string += c
            if c in RDR_MACROS:
                break
            if c in COLL_OPENERS or c in COLL_CLOSERS:
                break
            c = self.fd.read(1)
            self.col_after_1_based += 1
        if c in WHITESPACE:
            self.back1()
            self.col_after_1_based -= 1
        elif c == EOF_SIGNAL:
            self.col_after_1_based = self.fd.tell() + 1
        return start_col_1, string

    def next(self) -> Token:
        c1, s = self.get_non_white()
        if m := re.match(int_pat, s):
            result = Token(self.line, c1, INT_TT, int(m.group(0)))
            return result
        elif m := re.match(sym_pat, s):
            result = Token(self.line, c1, SYM_TT, m.group(0))
            return result
        elif s in COLL_OPENERS or s in COLL_CLOSERS:
            result = Token(self.line, c1, PNC_TT, s)
            return result
        return Token(-1, -1, None, None)


def lex_str(input_str: str) -> List[Token]:
    lexer : LasrLexer = LasrLexer(io.StringIO(input_str))
    result : List[Token] = []
    token : Token = lexer.next()
    while token.val is not None:
        result.append(token)
        token = lexer.next()
    return result
