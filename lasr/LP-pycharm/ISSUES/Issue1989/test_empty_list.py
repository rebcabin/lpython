from lpython import dataclass

@dataclass
class Pattern:
    _foo : list[tuple[str]]

foo : list[tuple[str]] = []

pat : Pattern = Pattern([('',)])
