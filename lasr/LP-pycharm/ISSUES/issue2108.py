from lpython import (i8, # i32, i64, f32, f64,
                     dataclass
                     )
from numpy import (empty,
                   int8,
                   )

r : i8 = i8(240)

@dataclass
class Foo:
    a : i8[4] = empty(4, dtype=int8)

foo : Foo = Foo()
foo.a = empty(4, dtype=int8)

############# ATTENTION: GENERATES DEPRECATION WARNING IN CPYTHON
# foo.a[0] = r
############# DOES NOT GENERATE WARNING IN CPYTHON
foo.a[0] = r - i8(256)

print(foo.a[0])