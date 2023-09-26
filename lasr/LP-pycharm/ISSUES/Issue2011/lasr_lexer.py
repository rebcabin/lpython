from lpython import (dataclass, InOut, i32,
                     # print,
                     # str, list, Union, bool
    )


NUMERICAL_NOISE : list[str] = ['o', 'O', 'b', 'B', 'x', 'X']


def in_(c: str, l: list[str]) -> bool:
    result : bool = False
    s : str
    for s in l:
        if s == c:
            result = True
            break
    return result


def strip_numerical_noise(s : str) -> str:
    """Assume input has been through 'match_integer'."""
    result : str = ''
    i : i32 = 0
    if s[0] == '0':
        if len(s) > 1 and in_(s[1], NUMERICAL_NOISE):
            i = 2
    j : i32
    for j in range(i, len(s)):
        if s[j] != '_':
            result += s[j]
    return result


I4C: dict[str, i32] = {
    '0': 0, '1': 1, '2': 2, '3': 3,
    '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9,
    'a': 10, 'b': 11, 'c': 12, 'd': 13,
    'A': 10, 'B': 11, 'C': 12, 'D': 13,
    'e': 14, 'f': 15,
    'E': 14, 'F': 15}


def cnvi(s : str, base : i32=10) -> i32:
    """Assume input has been through 'match_integer'."""
    assert base == 10 or base == 8 or base == 16 or base == 2
    result : i32 = 0
    c : str
    t : str = strip_numerical_noise(s)
    pow: i32 = base ** (len(t) - 1)
    for c in t:
        incr : i32 = pow * I4C[c]
        result += incr
        pow = (pow // base)
    return result


if __name__ == '__main__':
    assert cnvi('0b0', base=2) == 0
    assert cnvi('0b1', base=2) == 1
    assert cnvi('0b10', base=2) == 2
    assert cnvi('0b11', base=2) == 3
    assert cnvi('0b1111_0100_111', base=2) == 1959
    assert cnvi('0b7a7', base=16) == 1959
    
