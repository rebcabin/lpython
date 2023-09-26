from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass)
from numpy import empty, sqrt, float32, float64, int8, array


@dataclass
class LPBHV_small:
    dim : i32 = 4
    a : i8[4] = empty(4, dtype=int8)


def g() -> None:
    l2 : LPBHV_small = LPBHV_small(
        4,
        array([214, 157, 3, 146],dtype=int8))
        # [i8(214), i8(157), i8(3), i8(146)])


if __name__ == "__main__":
    print("Module HDC")
    print('')
    g()
