from lpython import dataclass, i32

@dataclass
class foo:
    """docstring"""
    bar : i32 = 0

@dataclass
class bar:
    """docstring"""
    baz : i32 = 42
