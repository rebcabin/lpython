from typing import Optional


from pydantic.annotated_types import Any, Dict


from lpython import i32


import lasr_lexer as ll


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


FullForm = Dict[str, Any | Dict[str, Any]]


#   _  _         _       _____
#  | \| |___  __| |___  |_   _|  _ _ __  ___ ___
#  | .` / _ \/ _` / -_)   | || || | '_ \/ -_|_-<
#  |_|\_\___/\__,_\___|   |_| \_, | .__/\___/__/
#                             |__/|_|
#
# Corresponding to "terms" in the ASDL for ASR,
# on the left-hand sides of equals signs.


TTYPE_NT : str = "ttype"


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


INTEGER_KINDS   : set[i32] = {1, 2, 4, 8}
LOGICAL_KINDS   : set[i32] = {1, 2, 4}
REAL_KINDS      : set[i32] = {4, 8}
COMPLEX_KINDS   : set[i32] = {4, 8}
CHARACTER_KINDS : set[i32] = {1}


#   ___            _                   _        _   _
#  |_ _|_ __  _ __| |___ _ __  ___ _ _| |_ __ _| |_(_)___ _ _  ___
#   | || '  \| '_ \ / -_) '  \/ -_) ' \  _/ _` |  _| / _ \ ' \(_-<
#  |___|_|_|_| .__/_\___|_|_|_\___|_||_\__\__,_|\__|_\___/_||_/__/
#            |_|


class Node:

    def __init__(self, lexer: Optional[ll.LasrLexer] = None):
        self.lexer : ll.LasrLexer = lexer
        self.line  : ll.Line = 1
        self.col   : ll.Col = 1

    def parse(self) -> None:
        raise NotImplementedError

    def full_form(self) -> FullForm:
        raise NotImplementedError

    def must_be(self, v: ll.LTVal) -> bool:
        token : ll.Token = self.lexer.next()
        self.line = token.line_1
        self.col  = token.col_start_1
        if v != token.val:
            print(f'Syntax error on line {token.line_1}, column {token.col_start_1}')
            print(f'Token Value must be {v}, not {token.val}')
            return False
        return True

    def get_of_type(self, tt: ll.LTType) -> ll.LTVal:
        token : ll.Token = self.lexer.next()
        self.line = token.line_1
        self.col  = token.col_start_1
        if tt != token.type:
            print(f'Syntax error on line {token.line_1}, column {token.col_start_1}')
            print(f'Token Type must be {tt}, not {token.type}')
            return None
        return token.val


Multiplicity = Optional[str]


MULTIPLICITY_ZERO_OR_MORE = "*"
MULTIPLICITY_ONE_OR_MORE  = "+"
MULTIPLICITY_ZERO_OR_ONE  = "?"


class MultiplicityNode(Node):

    def __init__(self, lexer: Optional[ll.LasrLexer] = None):
        super().__init__(lexer)
        self.multiplicity : Multiplicity   = None
        self.emptyQ       : Optional[bool] = None


class Dimensions(MultiplicityNode):
    """A Multiplicity node does not appear explicitly
    in the grammar. If `expr` is in the grammar, then
    its multiplicity nodes are `expr*`, `expr?`, and
    `expr+`."""
    def __init__(self,
                 lexer: Optional[ll.LasrLexer] = None,
                 contents: Any = None):
        super().__init__(lexer)
        self.multiplicity = MULTIPLICITY_ZERO_OR_MORE
        self.contents = contents
        self.emptyQ = (contents is None)

    def __eq__(self, other):
        if self.emptyQ and other.emptyQ:
            return True
        raise NotImplementedError

    def parse(self) -> "Dimensions":
        self.must_be(ll.VECT_OPEN)
        self.contents = None
        # TODO: contents
        self.must_be(ll.VECT_CLOSE)
        self.emptyQ = True
        return self

    def full_form(self) -> FullForm:
        result = {"contents": self.contents}
        return result


class TType(Node):

    def __init__(self, lexer: Optional[ll.LasrLexer] = None):
        super().__init__(lexer)

    def parse(self) -> Optional["TType"]:
        self.must_be(ll.LIST_OPEN)
        variety = self.get_of_type(ll.SYM_TT)
        if variety == INTEGER_TTYPE:
            kind = self.get_of_type(ll.INT_TT)
            if kind not in INTEGER_KINDS:
                print(f'Syntax error on line {self.line}, column {self.col}')
                print(f'Integer kind must be one of {INTEGER_KINDS}, '
                      f'not {kind}')
            result = Integer(self.lexer, kind=4)
        else:
            raise NotImplementedError
        result.dimensions = Dimensions(self.lexer).parse()
        if result.dimensions is None:
            pass
        self.must_be(ll.LIST_CLOSE)
        return result


class Integer(TType):

    def __init__(self,
                 lexer: Optional[ll.LasrLexer] = None,
                 kind: int = 0):
        super().__init__(lexer)
        self.kind       : int                  = kind
        self.dimensions : Optional[Dimensions] = None

    # From the MASR prototype:
    #
    # (s/valid? ::asr/asr-term
    #     {::asr/term ::asr/ttype,
    #         ::asr/asr-ttype-head
    #         {::asr/ttype-head   ::asr/Integer,
    #             ::asr/integer-kind 4
    #             ::asr/dimension*   []}}

    # The pydantic equivalent of a clojure .spec is
    # a pydantic.dataclass.

    def full_form(self) -> FullForm:
        result : FullForm = \
            {"term"           : "ttype",
             "asr_ttype_head" :
             {"ttype_head"    : "Integer",
              "integer_kind"  : self.kind,
              "dimensions"    : self.dimensions.full_form()}}
        return result
