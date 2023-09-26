from io import StringIO


from lasr_lexer import (
    LasrLexer, LTType, LTVal, Token,
    INT_TT, FLT_TT, SYM_TT, PNC_TT,
    MCR_TT, NKW_TT, QKW_TT, AKW_TT, lex_str)


from lpython import InOut


def dig_toks(line: int, col: int,
             tipe: LTType, val: LTVal,
             input: str):
    tok = LasrLexer(StringIO(input))
    token : Token = tok.next()
    while token.val != val:
        if token.val is None:
            break
        token = tok.next()

    assert token.line_1 == line
    assert token.col_start_1  == col
    assert token.type == tipe
    assert token.val  == val


cases = [
    # lin col ttype       val  input
    (1,  1, INT_TT,        42, '42'),
    (1,  3, INT_TT,        43, '  43  '),
    (2,  3, INT_TT,        44, '    foo\n  44\n'),
    (1,  5, SYM_TT,     "foo", '    foo\n  44'),
    (1,  1, PNC_TT,       "(", '(Integer 4 [])'),
    (1,  2, SYM_TT, "Integer", '(Integer 4 [])'),
    (1, 10, INT_TT,         4, '(Integer 4 [])'),
    (1, 12, PNC_TT,       "[", '(Integer 4 [])'),
    (1, 13, PNC_TT,       "]", '(Integer 4 [])'),
    (1, 14, PNC_TT,       ")", '(Integer 4 [])'),
    ]


def test_lex():

    ttq : LasrLexer
    t : str  # Issue 1991 -- no dummy value needed in CPython

    ttq = LasrLexer(StringIO('  foo  bar  '))
    ttq.eat_white()
    t = ttq.peek()
    assert t == 'f'

    for case in cases:
        dig_toks(*case)

    ttq = LasrLexer(StringIO('(Integer 4 [])'))
    c, t = ttq.get_non_white()
    assert t == '('
    assert c == 1
    c, t = ttq.get_non_white()
    assert t == 'Integer'
    assert c == 2
    c, t = ttq.get_non_white()
    assert t == '4'
    assert c == 10
    c, t = ttq.get_non_white()
    assert t == '['
    assert c == 12
    c, t = ttq.get_non_white()
    assert t == ']'
    assert c == 13
    c, t = ttq.get_non_white()
    assert t == ')'
    assert c == 14
    # Bounce off the end
    c, t = ttq.get_non_white()
    assert t == ''
    assert c == 15
    c, t = ttq.get_non_white()
    assert t == ''
    assert c == 15

    tts : list[Token] = lex_str('(Integer 4 [])')
    assert tts == [
        Token(1,  1, PNC_TT, "("),
        Token(1,  2, SYM_TT, "Integer"),
        Token(1, 10, INT_TT, 4),
        Token(1, 12, PNC_TT, "["),
        Token(1, 13, PNC_TT, "]"),
        Token(1, 14, PNC_TT, ")"),
        ]

    pass

