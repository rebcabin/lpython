from random import random

from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass,
                     # random
                     )
from numpy import (empty, sqrt, float32, float64,
                   int8, int32, array, # ndarray
                   )


HDC_DIM: Const[i32] = 8192


BITS_PER_BYTE : list[i32] = \
    [0, 1, 1, 2,
     1, 2, 2, 3,
     1, 2, 2, 3,
     2, 3, 3, 4]


NIBBLE_HAMMINGS : list[list[i32]] = [
    # 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
     [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4], # 0
     [1, 0, 2, 1, 2, 1, 3, 2, 2, 1, 3, 2, 3, 2, 4, 3], # 1
     [1, 2, 0, 1, 2, 3, 1, 2, 2, 3, 1, 2, 3, 4, 2, 3], # 2
     [2, 1, 1, 0, 3, 2, 2, 1, 3, 2, 2, 1, 4, 3, 3, 2], # 3
     [1, 2, 2, 3, 0, 1, 1, 2, 2, 3, 3, 4, 1, 2, 2, 3], # 4
     [2, 1, 3, 2, 1, 0, 2, 1, 3, 2, 4, 3, 2, 1, 3, 2], # 5
     [2, 3, 1, 2, 1, 2, 0, 1, 3, 4, 2, 3, 2, 3, 1, 2], # 6
     [3, 2, 2, 1, 2, 1, 1, 0, 4, 3, 3, 2, 3, 2, 2, 1], # 7
     [1, 2, 2, 3, 2, 3, 3, 4, 0, 1, 1, 2, 1, 2, 2, 3], # 8
     [2, 1, 3, 2, 3, 2, 4, 3, 1, 0, 2, 1, 2, 1, 3, 2], # 9
     [2, 3, 1, 2, 3, 4, 2, 3, 1, 2, 0, 1, 2, 3, 1, 2], # A
     [3, 2, 2, 1, 4, 3, 3, 2, 2, 1, 1, 0, 3, 2, 2, 1], # B
     [2, 3, 3, 4, 1, 2, 2, 3, 1, 2, 2, 3, 0, 1, 1, 2], # C
     [3, 2, 4, 3, 2, 1, 3, 2, 2, 1, 3, 2, 1, 0, 2, 1], # D
     [3, 4, 2, 3, 2, 3, 1, 2, 2, 3, 1, 2, 1, 2, 0, 1], # E
     [4, 3, 3, 2, 3, 2, 2, 1, 3, 2, 2, 1, 2, 1, 1, 0]] # F


HEX_CHARS : list[str] = [
    '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


# Issue 2066
n = TypeVar("n")


# Issue 2107
# @dataclass
# class LnBhv:
#     dim : i32
#     a : i8[n]


@dataclass
class LpBhv:
    # Issue 2083: can't say HDC_DIM
    dim : i32 = 8192
    a : i8[8192] = empty(8192, dtype=int8)


def hamming_lp_bhv(this : LpBhv, that : LpBhv) -> i32:
    i : i32
    assert this.dim == that.dim
    result : i32 = 0
    for i in range(this.dim):
        # WATCH OUT for operator precedence:
        # >> binds tighter than &; parenthesize EVERYTHING
        low1 : i32 =  (i32(this.a[i]) & 0x0F)
        hig1 : i32 = ((i32(this.a[i]) & 0xF0) >> 4)

        low2 : i32 =  (i32(that.a[i]) & 0x0F)
        hig2 : i32 = ((i32(that.a[i]) & 0xF0) >> 4)

        result += NIBBLE_HAMMINGS[low1][low2]
        result += NIBBLE_HAMMINGS[hig1][hig2]

    return result


def coin_flip(probability : f64=f64(0.5)) -> i8:
    """roll 1 bit"""
    result : i8 = i8(0)
    r : f64 = random()
    if r < probability:
        result = i8(1)
    return result


def random_lp_bhv(bit_probability : f64=f64(0.5)) -> LpBhv:
    """factory"""
    lp_bhv : LpBhv = LpBhv()
    # Issue 2104 : all instances share storage by default
    lp_bhv.a = empty(8192, dtype=int8)
    i : i32
    for i in range(lp_bhv.dim):
        lp_bhv.a[i] = i8(0)
    return lp_bhv


def roll_bits(bit_probability : f64=f64(0.5)) -> i8:
    result : i8 = i8(0)



def h() -> None:
    i : i32
    for i in range(8):
        coin : i8 = coin_flip(0.5)
        print(coin, end='')
    print('')

    print('')


@dataclass
class LpBhvSmall:
    dim : i32 = 4
    a : i8[4] = empty(4, dtype=int8)


def hamming_lp_bhv_small(this : LpBhvSmall, that : LpBhvSmall) -> i32:
    i : i32
    assert this.dim == that.dim
    result : i32 = 0
    for i in range(this.dim):
        # WATCH OUT for operator precedence:
        # >> binds tighter than &; parenthesize EVERYTHING
        low1 : i32 =  (i32(this.a[i]) & 0x0F)
        hig1 : i32 = ((i32(this.a[i]) & 0xF0) >> 4)

        low2 : i32 =  (i32(that.a[i]) & 0x0F)
        hig2 : i32 = ((i32(that.a[i]) & 0xF0) >> 4)

        # print('low1: ', end='')
        # print(HEX_CHARS[low1], end='')
        # print(', low2: ', end='')
        # print(HEX_CHARS[low2], end='')
        # print(', h: ', NIBBLE_HAMMINGS[low1][low2])

        # print('hig1: ', end='')
        # print(HEX_CHARS[hig1], end='')
        # print(', hig2: ', end='')
        # print(HEX_CHARS[hig2], end='')
        # print(', h: ', NIBBLE_HAMMINGS[hig1][hig2])

        result += NIBBLE_HAMMINGS[low1][low2]
        result += NIBBLE_HAMMINGS[hig1][hig2]

        # print('result so far: ', result)

    return result


def distance_lp_bhv_small(this : LpBhvSmall, that : LpBhvSmall) -> f64:
    h : i32 = hamming_lp_bhv_small(this, that)
    print('h: ', end=''); print(h)
    print('64-bit distance')
    result : f64 = f64(h)
    print(result)
    print(f64(this.dim))
    result /= f64(this.dim)
    print(result)

    print('32-bit distance')
    result3 : f32 = f32(h)
    print(result3)
    print(f32(this.dim))
    result3 /= f32(this.dim)
    print(result3)

    return result


def print_fully_lp_bhv_small(lphv_small : LpBhvSmall) -> None:
    i : i32
    print("DECIMAL")
    print(lphv_small.a)
    print('')
    print("HEX (VERIFIED AGAINST CPYTHON)")
    for i in range(4):
        elt : i32 = i32(lphv_small.a[i])
        hx : str = hex(elt)
        print(hx, end=' ')
        bn : str = bin(elt)
        print(bn)
    print('')
    print("BITS (VERIFIED AGAINST CPYTHON)")
    for i in range(4):
        elt : i32 = i32(lphv_small.a[i])
        elt &= i32(0xff)
        hx : str = hex(elt)
        print(hx, end=' ')
        bn : str = bin(elt)
        print(bn)
    print('')


def g() -> None:
    l1 : LpBhvSmall = LpBhvSmall()
    l1.a = empty(4, dtype=int8)
    l1.a[0] = i8(-96)
    l1.a[1] = i8(-17)
    l1.a[2] = i8(80)
    l1.a[3] = i8(107)
    print_fully_lp_bhv_small(l1)

    assert l1.a[0] == i8(-96)
    assert l1.a[1] == i8(-17)
    assert l1.a[2] == i8(80)
    assert l1.a[3] == i8(107)

    l2 : LpBhvSmall = LpBhvSmall() # Issue 2102 can't initialize
    # 4, empty(4, dtype=int8))
    l2.a = empty(4, dtype=int8)
    l2.a[0] = i8(-42)
    l2.a[1] = i8(-99)
    l2.a[2] = i8(3)
    l2.a[3] = i8(-110)
    print_fully_lp_bhv_small(l2)

    assert l2.a[0] == i8(-42)
    assert l2.a[1] == i8(-99)
    assert l2.a[2] == i8(3)
    assert l2.a[3] == i8(-110)

    # Issue 2104 -- CPython (but not LPython )overwrites when a is shared
    assert l1.a[0] == i8(-96)
    assert l1.a[1] == i8(-17)
    assert l1.a[2] == i8(80)
    assert l1.a[3] == i8(107)

    print('HAMMING DISTANCE')
    print(hamming_lp_bhv_small(l1, l2))
    print(distance_lp_bhv_small(l1, l2))
    print('')


def modify(b: f64[:], n: i32) -> f64[n]:
    return sqrt(b)


# Issue 2072; workaround is f64 instead of f32
def verify(a: f64[:], b: f64[:], result: f64[:], size: i32):
    i: i32
    eps: f64
    eps = f64(1e-6)

    for i in range(size):
        check : f64 = abs(a[i] * a[i] + sqrt(b[i]) - result[i])

        if not check <= eps or i == 5792:
            print("a[", end='')
            print(i, end='')
            print("] = ", end='')
            print(a[i], end='')
            print(", b[", end='')
            print(i,end='')
            print("] = ", end='')
            print(b[i])
            print("a[", end='')
            print(i, end='')
            print("] * a[", end='')
            print(i, end='')
            print("] + sqrt(b[", end='')
            print(i, end='')
            print("]) = ", end='')
            print(a[i] * a[i] + sqrt(b[i]))
            print("a[", end='')
            print(i, end='')
            print("] ** 2      + sqrt(b[", end='')
            print(i, end='')
            print("]) = ", end='')
            print(result[i])
            print('')

        assert check <= eps


def f():
    i: i32
    j: i32

    # Issue 2067
    a: f64[8192] = empty(HDC_DIM, dtype=float64)
    b: f64[8192] = empty(HDC_DIM, dtype=float64)
    c: f64[8192] = empty(HDC_DIM, dtype=float64)

    for i in range(HDC_DIM):
        a[i] = f64(i)

    # print(a)

    for j in range(HDC_DIM):
        b[j] = f64(j + 5)

    c = a ** f64(2) + modify(b, HDC_DIM)
    verify(a, b, c, HDC_DIM)


if __name__ == "__main__":

    print("Module HDC")
    print('SMALL HAMMING')
    g()

    print('LARGE RANDOM HAMMING')
    h()

    print('FLOATING-POINT VERIFICATION')
    f()
