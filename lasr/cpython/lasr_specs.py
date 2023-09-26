from typing import Literal


import pydantic
from pydantic import BaseModel
from pydantic.annotated_types import Any
from pydantic.class_validators import Union


class Dimensions_spec(BaseModel):
    contents : Any


class Integer_spec(BaseModel):
    ttype_head   : Literal["Integer"]
    integer_kind : int
    dimensions   : Dimensions_spec


class Real_spec(BaseModel):
    ttype_head : Literal["Real"]
    real_kind  : int
    dimensions : Dimensions_spec


class TType_spec(BaseModel):
    term : Literal['ttype']
    asr_ttype_head: Union[Integer_spec, Real_spec] = \
        pydantic.Field(discriminatior='ttype_head')
