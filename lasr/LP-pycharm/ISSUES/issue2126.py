from lpython import (i8, i32, i64, f32, f64,
                     dataclass
                     )
from numpy import (empty,
                   int8,
                   # all,  # Issue 2136
                   )

r : i8 = i8(240)

@dataclass
class Foo:
    a : i8[4] = empty(4, dtype=int8)
    dim : i32 = 4

def trinary_majority(x : Foo, y : Foo, z : Foo) -> Foo:
    foo : Foo = Foo()

    # Issue 2132
    # assert foo.dim == x.dim == y.dim == z.dim

    assert foo.dim == x.dim
    assert x.dim == y.dim
    assert y.dim == z.dim

    i : i32
    for i in range(foo.dim):
        foo.a[i] = (x.a[i] & y.a[i]) | (y.a[i] & z.a[i]) | (z.a[i] & x.a[i])

    # Issue 2130
    # foo.a = x.a | y.a | z.a
    # foo.a = (x.a & y.a) | (y.a & z.a) | (z.a & x.a)
    return foo


t1 : Foo = Foo()
t1.a = empty(4, dtype=int8)

t2 : Foo = Foo()
t2.a = empty(4, dtype=int8)

t3 : Foo = Foo()
t3.a = empty(4, dtype=int8)

r1 : Foo = trinary_majority(t1, t2, t3)

def assert_all_equal(a : Foo, b : Foo):
    """Issue2136"""
    i : i32
    for i in range(a.dim):
        assert a.a[i] == b.a[i]

assert_all_equal(r1, t1)
# Issue 2136
# assert all(r1.a == t1.a)
