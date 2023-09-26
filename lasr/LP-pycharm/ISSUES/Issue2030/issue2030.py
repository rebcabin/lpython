from lpython import dataclass

FOO : str = 'foo'

@dataclass
class bar:
    baz : str = FOO
