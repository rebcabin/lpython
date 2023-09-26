from lpython import (i8, i32, i64, f32, f64,
                     TypeVar, Const,
                     dataclass)
from numpy import empty, sqrt, float32, float64, int8


# Issue 2066
n = TypeVar("n")


# Issue 2072; workaround is f64 instead of f32
@dataclass
class LPBHV_small:
    dim : i32 = 4
    a : i8[4] = empty(4, dtype=int8)


def as_hex(lphv_small : LPBHV_small) -> None:
    i : i32
    for i in range(4):
        hx : str = hex(lphv_small.a[i])
        print(hx)

def g() -> None:
    lpbhv_small : LPBHV_small = LPBHV_small()
    print(lpbhv_small.a)
    as_hex(lpbhv_small)


if __name__ == "__main__":
    print("Module HDC")
    g()
