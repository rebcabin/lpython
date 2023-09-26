from random import (random,
                    # seed  # Issue 2110
                    )

from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass,
                     # random
                     )
from numpy import (empty, sqrt, float32, float64,
                   int8, int32, array, # ndarray
                   )


BITS_FOR_EACH_NIBBLE : list[i32] = \
    [0, 1, 1, 2,
     1, 2, 2, 3,
     1, 2, 2, 3,
     2, 3, 3, 4]

BITS_PER_BYTE : i32 = 8

BYTES : i32 = 1  # unit of measure

HDC_DIM: i32 = 1024 * BYTES

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


BIN_CHARS : list[str] = [
    '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
    '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111',
    ]


# Issue 2066
n = TypeVar("n")


# Issue 2107
# @dataclass
# class LnBhv:
#     dim : i32
#     a : i8[n]


#   _                         _____ _ ___ ___   _    _ _     __
#  | |   __ _ _ _ __ _ ___   / ( _ ) / _ \_  ) | |__(_) |_ __\ \
#  | |__/ _` | '_/ _` / -_) | |/ _ \ \_, // /  | '_ \ |  _(_-<| |
#  |____\__,_|_| \__, \___| | |\___/_|/_//___| |_.__/_|\__/__/| |
#                |___/       \_\                             /_/

@dataclass
class LpBhv:
    # Issue 2083: can't say HDC_DIM or BYTES
    dim : i32 = 1024  # BYTES
    a : i8[1024] = empty(1032, dtype=int8)


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


def distance_lp_bhv(this : LpBhv, that : LpBhv, debug : bool=False) -> f64:
    h : i32 = hamming_lp_bhv(this, that)
    if debug:
        print('h: ', end=''); print(h)
        print('64-bit distance (expect roughly 0.5)')
    result : f64 = f64(h)
    if debug:
        print(result)
        print(f64(this.dim * BITS_PER_BYTE))
    result /= f64(this.dim * BITS_PER_BYTE)
    if debug:
        print(result)

        print('32-bit distance (expect roughly 0.5)')
        result3 : f32 = f32(h)
        print(result3)
        print(f32(this.dim * BITS_PER_BYTE))
        result3 /= f32(this.dim * BITS_PER_BYTE)
        print(result3)

        print('')

    return result


def coin_flip(probability : f64=f64(0.5)) -> i8:
    """roll 1 bit"""
    result : i8 = i8(0)
    r : f64 = random()
    if r < probability:
        result = i8(1)
    return result


def random_byte(bit_probability : f64=f64(0.5)) -> i8:
    _ : f64 = random()  # Get some variation
    _ = random()  # lame attempt at entropy
    _ = random()
    _ = random()
    result : i8 = i8(0)
    i : i32
    for i in range(BITS_PER_BYTE):
        c : i8 = coin_flip(bit_probability)
        result |= (c << i8(i))
    return result


def print_some_lp_bhv(bhv : LpBhv, as_hex : bool) -> None:
    i : i32
    if as_hex:
        for i in range(4):
            print(byte_as_hex(bhv.a[i], debug=False), end=' ')
        print('...', end=' ')
        for i in range(1020, 1024):
            print(byte_as_hex(bhv.a[i], debug=False), end=' ')
        print('')
    else:
        for i in range(4):
            print(byte_as_bin(bhv.a[i], debug=False), end=' ')
        print('...', end=' ')
        for i in range(1020, 1024):
            print(byte_as_bin(bhv.a[i], debug=False), end=' ')
        print('')


def random_lp_bhv(bit_probability : f64=f64(0.5)) -> LpBhv:
    """factory"""
    lp_bhv : LpBhv = LpBhv()
    # Issue 2104 : all instances share storage by default
    lp_bhv.a = empty(HDC_DIM, dtype=int8)
    i : i32
    for i in range(lp_bhv.dim):
        b : i8 = random_byte(0.5)
        if b > i8(127):
            lp_bhv.a[i] = b - i8(256)  # Issue 2114
        else:
            lp_bhv.a[i] = b  # Issue 2114
    return lp_bhv


def zero_lp_bhv() -> LpBhv:
    """factory"""
    lp_bhv : LpBhv = LpBhv()
    # Issue 2104 : all instances share storage by default
    lp_bhv.a = empty(HDC_DIM, dtype=int8)
    i : i32
    for i in range(lp_bhv.dim):
        lp_bhv.a[i] = i8(0)
    return lp_bhv


def ones_lp_bhv() -> LpBhv:
    """factory"""
    lp_bhv : LpBhv = LpBhv()
    # Issue 2104 : all instances share storage by default
    lp_bhv.a = empty(HDC_DIM, dtype=int8)
    i : i32
    for i in range(lp_bhv.dim):
        lp_bhv.a[i] = i8(255) - i8(256)  # Issue 2114
    return lp_bhv


def large_hamming_tryst() -> None:
    print('LARGE RANDOM HAMMING')
    i : i32
    print('EIGHT COIN FLIPS @ 0.5 bit-probability')
    for i in range(8):
        coin : i8 = coin_flip(0.5)
        print(coin, end='')
    print('')
    print('')

    print('ONE RANDOM BYTE @ 0.5 bit-probability')
    r : i8 = random_byte(0.5)
    hexubbus : str = byte_as_hex(r, debug=True)
    # only in LPython
    # assert hexubbus == 'E6'

    print('SOME RANDOM BYTES from 1024')
    a : LpBhv = random_lp_bhv(0.5)
    print_some_lp_bhv(a, as_hex=True)
    print('')

    b : LpBhv = random_lp_bhv(0.5)
    print('HAMMING DISTANCE a <-> b (LARGE)')
    print('expect roughly 4096, half of 8192 bits')
    hab : i32 = hamming_lp_bhv(a, b)
    print(hab)
    print('floating-point distance; expect roughly 0.5')
    dab : f64 = distance_lp_bhv(a, b, debug=False)
    print(dab)
    print('')

    print('HAMMING DISTANCE a <-> 0 (LARGE)')
    print('expect roughly 4096, half of 8192 bits')
    h0 : i32 = hamming_lp_bhv(a, zero_lp_bhv())
    print(h0)
    print('floating-point distance; expect roughly 0.5')
    d0 : f64 = distance_lp_bhv(a, zero_lp_bhv(), debug=False)
    print(d0)
    print('')

    print('HAMMING DISTANCE a <-> 1 (LARGE)')
    print('expect exactly 8192-', end='')
    print(h0, end=' = '); print(8192-h0)
    h1 : i32 = hamming_lp_bhv(a, ones_lp_bhv())
    print(h1)
    assert h1 == 8192 - h0
    print('floating-point distance; expect roughly 0.5')
    d1 : f64 = distance_lp_bhv(a, ones_lp_bhv(), debug=False)
    print(d1)
    print('')


def byte_as_(r : i8, chars : list[str], debug : bool) -> str:
    norm: i32 = (i32(r) & 0xFF)
    left: i32 = ((i32(r) & 0xF0) >> 4)
    right: i32 = (i32(r) & 0x0F)
    if debug:
        print('[normed_i8, high_nibble, low_nibble]: ', end='')
        print([i32(norm), left, right])
    left_ : str = chars[i32(left)]
    if debug:
        print(left_, end='')
    right_ : str = chars[i32(right)]
    if debug:
        print(right_, end='')
        print('')
        print('')
    result : str = left_ + right_
    return result


def byte_as_hex(r : i8, debug : bool) -> str:
    return byte_as_(r, HEX_CHARS, debug)


def byte_as_bin(r : i8, debug : bool) -> str:
    return byte_as_(r, BIN_CHARS, debug)


def ternary_majority(x : LpBhv, y : LpBhv, z : LpBhv) -> LpBhv:
    lp_bhv : LpBhv = LpBhv()
    lp_bhv.a = empty(lp_bhv.dim, dtype=int8)
    # Issue 2130
    # lp_bhv.a = x.a | y.a | z.a
    # lp_bhv.a = (x.a & y.a) | (y.a & z.a) | (z.a & x.a)
    i : i32
    for i in range(lp_bhv.dim):
        lp_bhv.a[i] = (x.a[i] & y.a[i]) | \
                      (y.a[i] & z.a[i]) | \
                      (z.a[i] & x.a[i])
    return lp_bhv


def binary_majority(x : LpBhv, y : LpBhv) -> LpBhv:
    tieb : LpBhv = random_lp_bhv(0.5)
    return ternary_majority(x, y, tieb)


def mul_bhv(x : LpBhv, y : LpBhv) -> LpBhv:
    lp_bhv : LpBhv = LpBhv()
    lp_bhv.a = empty(lp_bhv.dim, dtype=int8)
    i : i32
    for i in range(lp_bhv.dim):
        lp_bhv.a[i] = x.a[i] ^ y.a[i]
    return lp_bhv


def assert_all_equal(a : LpBhv, b : LpBhv):
    """Issue2136"""
    i : i32
    for i in range(a.dim):
        assert a.a[i] == b.a[i]


def large_majority_tryst() -> None:
    print("LARGE MAJORITY TEST")
    print('no assert is a good result')
    print('')
    ones : LpBhv = ones_lp_bhv()
    zero : LpBhv = zero_lp_bhv()
    rnds : LpBhv = random_lp_bhv(0.5)

    tr00 : LpBhv = ternary_majority(rnds, zero, zero)
    # Issue 2135, 2136
    # assert tr00.a == rnds.a
    assert_all_equal(tr00, zero)

    # sanity checks
    tr01 : LpBhv = ternary_majority(rnds, ones, zero)
    assert_all_equal(tr01, rnds)

    rnd2 : LpBhv = random_lp_bhv(0.5)
    tieb : LpBhv = random_lp_bhv(0.5)

    # majority sum with tiebreaker
    trXY : LpBhv = ternary_majority(rnds, rnd2, tieb)

    print('a, b, c, a (+) b (+) c [majority sum]')
    print_some_lp_bhv(rnds, as_hex=True)
    print_some_lp_bhv(rnd2, as_hex=True)
    print_some_lp_bhv(tieb, as_hex=True)
    print_some_lp_bhv(trXY, as_hex=True)
    print('')

    print('a, b, c, a (+) b (+) c [majority sum]')
    print_some_lp_bhv(rnds, as_hex=False)
    print_some_lp_bhv(rnd2, as_hex=False)
    print_some_lp_bhv(tieb, as_hex=False)
    print_some_lp_bhv(trXY, as_hex=False)
    print('')


def distributivity_tryst() -> None:
    print('DISTRIBUTIVITY TEST')
    a : LpBhv = random_lp_bhv(0.5)
    b : LpBhv = random_lp_bhv(0.5)
    c : LpBhv = random_lp_bhv(0.5)
    x : LpBhv = random_lp_bhv(0.5)
    a_b_c : LpBhv = ternary_majority(a, b, c)
    x__a_b_c : LpBhv = mul_bhv(x, a_b_c)
    print('dist a a_b_c        (expect 0.25)', end=': ')
    print(distance_lp_bhv(a, a_b_c, debug=False))
    print('dist b a_b_c        (expect 0.25)', end=': ')
    print(distance_lp_bhv(b, a_b_c, debug=False))
    print('dist c a_b_c        (expect 0.25)', end=': ')
    print(distance_lp_bhv(c, a_b_c, debug=False))
    print('dist x a_b_c        (expect 0.50)', end=': ')
    print(distance_lp_bhv(x, a_b_c, debug=False))

    print('dist a x__a_b_c     (expect 0.50)', end=': ')
    print(distance_lp_bhv(a, x__a_b_c, debug=False))
    print('dist b x__a_b_c     (expect 0.50)', end=': ')
    print(distance_lp_bhv(b, x__a_b_c, debug=False))
    print('dist c x__a_b_c     (expect 0.50)', end=': ')
    print(distance_lp_bhv(c, x__a_b_c, debug=False))
    print('dist x x__a_b_c     (expect 0.50)', end=': ')
    print(distance_lp_bhv(x, x__a_b_c, debug=False))

    xa : LpBhv = mul_bhv(x, a)
    xb : LpBhv = mul_bhv(x, b)
    xc : LpBhv = mul_bhv(x, c)
    xa_xb_xc : LpBhv = ternary_majority(xa, xb, xc)
    print('dist xa_xb_xc x__a_b_c (expect 0)', end=': ')
    print(distance_lp_bhv(xa_xb_xc, x__a_b_c, debug=False))


#   ___            _ _    _________   _    _ _     __
#  / __|_ __  __ _| | |  / /__ /_  ) | |__(_) |_ __\ \
#  \__ \ '  \/ _` | | | | | |_ \/ /  | '_ \ |  _(_-<| |
#  |___/_|_|_\__,_|_|_| | ||___/___| |_.__/_|\__/__/| |
#                        \_\                       /_/

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
    print('HAMMING DISTANCE (SMALL)')
    print('EXPECT ROUGHLY 16, HALF OF 32 bits = 4 bytes')
    h : i32 = hamming_lp_bhv_small(this, that)
    print('h: ', end=''); print(h)
    print('64-bit distance (expect roughly 0.5)')
    result : f64 = f64(h)
    print(result)
    print(f64(this.dim * BITS_PER_BYTE))
    result /= f64(this.dim * BITS_PER_BYTE)
    print(result)

    print('32-bit distance (expect roughly 0.5)')
    result3 : f32 = f32(h)
    print(result3)
    print(f32(this.dim * BITS_PER_BYTE))
    result3 /= f32(this.dim * BITS_PER_BYTE)
    print(result3)

    print('')

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


def small_hamming_tryst() -> None:
    print('SMALL HAMMING')
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

    _ : f64 = distance_lp_bhv_small(l1, l2)


#    __ _           _   _                       _     _
#   / _| |___  __ _| |_(_)_ _  __ _   _ __  ___(_)_ _| |_
#  |  _| / _ \/ _` |  _| | ' \/ _` | | '_ \/ _ \ | ' \  _|
#  |_| |_\___/\__,_|\__|_|_||_\__, | | .__/\___/_|_||_\__|
#                             |___/  |_|

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


def floating_point_tryst():
    print('FLOATING-POINT VERIFICATION')
    print('no assert is a good result')
    print('')

    i: i32
    j: i32

    # Issue 2067
    a: f64[1024] = empty(HDC_DIM, dtype=float64)
    b: f64[1024] = empty(HDC_DIM, dtype=float64)
    c: f64[1024] = empty(HDC_DIM, dtype=float64)

    for i in range(HDC_DIM):
        a[i] = f64(i)

    # print(a)

    for j in range(HDC_DIM):
        b[j] = f64(j + 5)

    c = a ** f64(2) + modify(b, HDC_DIM)
    verify(a, b, c, HDC_DIM)


if __name__ == "__main__":
    print("Module HDC")
    print('')

    floating_point_tryst()
    small_hamming_tryst()  # funny name so pytest doesn't pick it up
    large_hamming_tryst()
    large_majority_tryst()
    distributivity_tryst()
