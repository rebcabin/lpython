from lpython import dataclass, i32

@dataclass
class Node:
    line  : i32 = 0
    col   : i32 # workaround: add = 0
