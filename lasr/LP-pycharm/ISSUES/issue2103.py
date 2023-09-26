from lpython import (i8, i32, i64, f32, f64,
                     u8, u32,
                     TypeVar, Const,
                     dataclass
                     )

from numpy import (empty, sqrt, float32, float64,
                   int8, int32, array, # ndarray
                   )

def print_dict_i32(d : dict[str, i32]) -> None:
    print("{", end='')
    k : str
    v : i32
    for k, v in dict.items(d):
        print("\t'", end='')
        print(k, end='')
        print("':\t", end='')
        print(v, end='')
        print(",")
    print("}")

if __name__ == "__main__":

    d : dict[str, i32] = {'k': 42, 'l': 113}
    print_dict_i32(d)
