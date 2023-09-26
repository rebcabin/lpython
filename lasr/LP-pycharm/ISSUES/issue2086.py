from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass)
from numpy import empty, sqrt, float32, float64, int8


# Issue 2066
n = TypeVar("n")


HDC_DIM: Const[i32] = 8192


@dataclass
class LPBHV:
    # Issue 2083: can't say HDC_DIM
    dim : i32 = 8192
    a : u8[8192] = empty(8192, dtype=int8)


@dataclass
class LPBHV_small:
    dim : i32 = 4
    a : u8[4] = empty(4, dtype=int8)


def as_hex(lphv_small : LPBHV_small) -> None:
    i : i32
    print("HEX")
    for i in range(4):
        elt : u32 = u32(lphv_small.a[i])
        hx : str = hex(elt)
        print(hx, end='')
        print(' ' if i < 4 - 1 else '', end='')
    print('')
    print("BITS")
    for i in range(4):
        elt : u32 = u32(lphv_small.a[i])
        elt &= 0xff
        hx : str = hex(elt)
        print(hx, end='')
        print(' ' if i < 4 - 1 else '', end='')
    print('')


def g() -> None:
    lpbhv_small : LPBHV_small = LPBHV_small()
    print("DECIMAL")
    print(lpbhv_small.a)
    as_hex(lpbhv_small)


if __name__ == "__main__":
    print("Module HDC")
    g()
