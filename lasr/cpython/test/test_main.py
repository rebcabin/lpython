import dataclasses
from datetime import datetime
from typing import List, Optional
from pprint import pp

import pydantic.dataclasses
import pytest
from pydantic import ValidationError


from main import crack


def test_crack():
    assert crack() == 42


def test_pydantic():
    # ------------------------------------------------
    class User(pydantic.BaseModel):
        id        : int
        name      : str = 'John Doe'
        signup_ts : Optional[datetime] = None
        friends   : List[int] = []

    with pytest.raises(AttributeError):
        assert User.name == 'John Doe', \
            "Doesn't act like a class var."

    with pytest.raises(pydantic.ValidationError) as einfo:
        assert User().name == 'John Doe', \
            "Acts like an instance var, but fails" \
            "validation, missing a value for 'id'."
    print()
    print(einfo.value)
    # ------------------------------------------------
    external_data = {'id': '123',
                     'signup_ts': '2017-06-01 12:22',
                     'friends': [1, '2', b'3']}
    result = User(**external_data)
    user = result
    assert user is not None
    # ------------------------------------------------
    bad_data = {'id': 'FOOBAR',
                'signup_ts': '2017-06-01 12:22',
                'friends': [1, '2', b'3']}
    with pytest.raises(ValidationError) as einfo:
        result = User(**bad_data)
        assert result is None, "bad ID"
    print()
    print(einfo.value)
    # ------------------------------------------------
    assert isinstance(0xF00BA4, int)
    assert isinstance(int('0xF00BA4', base=16), int)

    weird_data = {'id': '0xF00BA4',
                  'signup_ts': '2017-06-01 12:22',
                  'friends': [1, '2', b'3']}

    weird_user = None
    with pytest.raises(ValidationError) as einfo:
        weird_user = User(**weird_data)
    print()
    print(einfo.value)
    assert weird_user is None, "can't parse hex!"
    # ------------------------------------------------


def class_instance_dicts(Xnym : str, X) -> None:
    print(f"\n__DICT__ OF CLASS {Xnym}")
    pp(X.__dict__)
    print(f"\n__DICT_ OF INSTANCE OF {Xnym}")
    pp(X().__dict__)


def test_class_and_instance_vars():
    # ------------------------------------------------
    class A:
        """dlass variables that get shadowed via
        monkey-patching"""
        x : int = 3
        y : int = 4
    class_instance_dicts("no instance vars A", A)
    a1 = A()
    a2 = A()
    a2.x = 7
    assert a1.x == 3, "access class var"
    assert A.x == 3, "class var still exists"
    assert a2.x == 7, "monkey-patched instance var"

    # ------------------------------------------------
    class B:
        """no class variables"""
        def __init__(self):
            self.x = 3
            self.y = 4
    class_instance_dicts("no classvars B", B)

    with pytest.raises(AttributeError) as einfo:
        assert B.x == 3, "no class variable"
    print()
    print(einfo.value)

    # ------------------------------------------------
    @pydantic.dataclasses.dataclass
    class C:
        """not really a dataclass?"""
        x : int = 3
        y : int = 4
    class_instance_dicts("pydantic dataclass C", C)

    assert C.x == 3, "has a class variable?"
    pp(C.__dict__)
    pp(C().__dict__)

    # ------------------------------------------------

    @dataclasses.dataclass
    class D:
        """no class variables"""
        x : int = 3
        y : int = 4
    class_instance_dicts("dataclass D", D)

    assert D.x == 3, "has class variable"
    assert D().x == 3, "has instnce variable"
