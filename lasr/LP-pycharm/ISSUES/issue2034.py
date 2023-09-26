from lpython import (i32, dataclass)

@dataclass
class FullFormValue:
    list_i32 : list[i32]
    string   : str

foo : dict[str, FullFormValue]

DEAD_LIST : list[i32] = [-1]  # Issue 2039 forces non-empty sentinel
DEAD_STRING : str = ''  # would prefer None but we don't have Optional

ttype    : FullFormValue = FullFormValue(DEAD_LIST, 'dimensions')
contents : FullFormValue = FullFormValue([1, 2], DEAD_STRING)

foo = {'ttype'   : ttype,
       'contents': contents}


# foo : dict[str, tuple[list[i32], str]]

# Issue 2041
# ttype    : tuple[list[i32], str] = ([-1], 'dimensions')
# contents : tuple[list[i32], str] = ([1, 2], '')

# foo = {'ttype': ([], 'dimensions'),
#        'contents' : ([1, 2], '')}
