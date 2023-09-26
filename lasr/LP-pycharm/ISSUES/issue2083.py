from lpython import (i8, i32, i64, f32, f64,
                     TypeVar, Const,
                     dataclass)


HDC_DIM: Const[i32] = 8192


@dataclass
class LPBHV:
    a : i8[HDC_DIM]
