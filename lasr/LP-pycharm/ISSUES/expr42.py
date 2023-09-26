from lpython import i32
assert hex(1959) == '0x7a7'
assert oct(1959) == '0o3647'
assert i32(1959) == 1959
assert i32('1959', base=10) == 1959
# assert i32('1959') == 1959 # Issue 2004
assert i32(hex(1959), base=16) == 1959
assert i32(oct(1959), base=8) == 1959
