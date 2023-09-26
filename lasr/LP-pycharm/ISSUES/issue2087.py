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
    a : i8[8192] = empty(8192, dtype=int8)


@dataclass
class LPBHV_small:
    dim : i32 = 4
    a : i8[4] = empty(4, dtype=int8)


def as_hex(lphv_small : LPBHV_small) -> None:
    i : i32
    print("HEX (VERIFIED)")
    for i in range(4):
        elt : i32 = i32(lphv_small.a[i])
        hx : str = hex(elt)
        print(hx, end=' ')
        bn : str = bin(elt)
        print(bn)
    print('')
    print("BITS (VERIFIED)")
    for i in range(4):
        elt : i32 = i32(lphv_small.a[i])
        elt &= i32(0xff)
        hx : str = hex(elt)
        print(hx, end=' ')
        bn : str = bin(elt)
        print(bn)
    print('')


def g() -> None:
    lpbhv_small : LPBHV_small = LPBHV_small()
    lpbhv_small.a[0] = i8(-96)
    lpbhv_small.a[1] = i8(-17)
    lpbhv_small.a[2] = i8(80)
    lpbhv_small.a[3] = i8(107)
    lpbhv_small.a[4] = i8(-42)
    print("DECIMAL")
    print(lpbhv_small.a)
    print('')
    as_hex(lpbhv_small)


if __name__ == "__main__":
    print("Module HDC")
    g()
