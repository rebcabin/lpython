from lpython import dataclass, i32

@dataclass
class foo:
    bar : list[i32] = []  ######### INCORRECT ###########
