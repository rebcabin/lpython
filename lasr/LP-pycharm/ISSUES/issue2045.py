from lpython import (dataclass, i32,
                     field, default_factory)

@dataclass
class Foo:
    string : str

@dataclass
class Bar :
    il : list[i32]
    foo : Foo = Foo('foo')

bar : Bar = Bar([1, 2, 3], Foo('bar'))