from io import StringIO
from pprint import pprint
from typing import Optional


import pydantic
import pytest


import lasr_parser as lp
import lasr_lexer  as ll
import lasr_specs  as ls


def test_integer_ttype_parse():
    integer : Optional[lp.Integer | lp.TType] = \
        lp.TType(ll.LasrLexer(StringIO('(Integer 4 [])'))).parse()
    assert isinstance(integer, lp.Integer)
    assert integer.kind == 4
    assert integer.dimensions is not None
    assert integer.dimensions.emptyQ
    assert integer.dimensions.contents is None
    assert integer.dimensions.multiplicity == \
           lp.MULTIPLICITY_ZERO_OR_MORE

    actual_ff = integer.full_form()
    expected_ff = {"term": "ttype",
                   "asr_ttype_head":
                       {"ttype_head": "Integer",
                        "integer_kind": 4,
                        "dimensions": lp.Dimensions().full_form()}}
    assert actual_ff == expected_ff

    actual_spec = ls.TType_spec(**actual_ff)
    expected_spec = ls.TType_spec(**expected_ff)
    assert actual_spec == expected_spec
    assert actual_spec.asr_ttype_head.ttype_head == "Integer"
    assert actual_spec.asr_ttype_head.integer_kind == 4
    assert actual_spec.asr_ttype_head.dimensions.contents is None


def test_negative_integer_ttype():

    with pytest.raises(NotImplementedError) as einfo:
        lp.TType(ll.LasrLexer(StringIO('(MISTAKE 4 [])'))).parse()
    print()
    pprint(einfo.value)

    expected_ff = {"term": "ttype",
                   "asr_ttype_head":
                       {"ttype_head": "MISTAKE",
                        "integer_kind": 4,
                        "dimensions": lp.Dimensions().full_form()}}

    with pytest.raises(pydantic.ValidationError) as einfo:
        ls.TType_spec(**expected_ff)
    print()
    pprint(einfo.value.errors())
