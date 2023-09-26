import lasr_lexer as ll
# from lasr_lexer import LasrLexer  # workaround


from lpython import i32, dataclass


@dataclass
class Node:
    lexer : ll.LasrLexer = ll.LasrLexer()
