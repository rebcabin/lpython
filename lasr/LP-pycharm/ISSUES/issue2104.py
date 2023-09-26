from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass
                     )

from numpy import (empty, sqrt, float32, float64,
                   int8, int32, array, # ndarray
                   )

@dataclass
class LpBhvSmall:
    dim : i32 = 4
    a : i8[4] = empty(4, dtype=int8)


def g() -> None:
    l1 : LpBhvSmall = LpBhvSmall() # Issue 2102 can't initialize
    # 4, empty(4, dtype=int8))
    l1.a = empty(4, dtype=int8)
    l1.a[0] = i8(-96)
    l1.a[1] = i8(-17)
    l1.a[2] = i8(80)
    l1.a[3] = i8(107)

    assert l1.a[0] == i8(-96)
    assert l1.a[1] == i8(-17)
    assert l1.a[2] == i8(80)
    assert l1.a[3] == i8(107)

    ################# ATTENTION: OVERWRITES l1.a in CPYTHON
    ################# BUT NOT IN LPYTHON

    l2 : LpBhvSmall = LpBhvSmall() # Issue 2102 can't initialize
    # 4, empty(4, dtype=int8))
    l2.a = empty(4, dtype=int8)
    l2.a[0] = i8(-42)
    l2.a[1] = i8(-99)
    l2.a[2] = i8(3)
    l2.a[3] = i8(-110)

    assert l2.a[0] == i8(-42)
    assert l2.a[1] == i8(-99)
    assert l2.a[2] == i8(3)
    assert l2.a[3] == i8(-110)

    assert l1.a[0] == i8(-96)
    assert l1.a[1] == i8(-17)
    assert l1.a[2] == i8(80)
    assert l1.a[3] == i8(107)


if __name__ == "__main__":
    g()
