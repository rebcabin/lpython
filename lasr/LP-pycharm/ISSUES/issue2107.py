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


def coin_flip(probability : f64=f64(0.5)) -> i8:
    """roll 1 bit"""
    result : i8 = i8(0)
    r : f64 = random()
    if r < probability:
        result = i8(1)
    return result


def h() -> None:
    i : i32
    for i in range(10):
        coin : i8 = coin_flip()
        print(coin, end='')
        print('')


if __name__ == "__main__":
    h()
