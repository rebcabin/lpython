# HAMMING DISTANCE
# low1: 0, low2: 6, h:  2
# hig1: 0, hig2: 6, h:  2
# result so far:  4
# low1: F, low2: D, h:  1
# hig1: F, hig2: D, h:  1
# result so far:  6
# low1: 0, low2: 3, h:  2
# hig1: 0, hig2: 3, h:  2
# result so far:  10
# low1: B, low2: 2, h:  2
# hig1: B, hig2: 2, h:  2
# result so far:  14
# 14

# Compute hamming distance by hand

#         ...  ..  5
# 0xa0 0b1010 0000    A 0
# 0xd6 0b1101 0110  - D 6
#                     3 2

#         ...   .  4
# 0xef 0b1110 1111    E F
# 0x9d 0b1001 1101  - 9 D
#                     3 1

#         . .   .. 4
# 0x50 0b0101 0000    5 0
# 0x03 0b0000 0011  - 0 3
#                     2 2

#        .... .  . 6
# 0x6b 0b0110 1011    6 B
# 0x92 0b1001 0010  - 9 2
#                     4 2

# should be 19

# DECIMAL
# -96 -17 80 107
#
# BITS (VERIFIED AGAINST CPYTHON)
# 0xa0 0b10100000
# 0xef 0b11101111
# 0x50 0b01010000
# 0x6b 0b01101011
#
# DECIMAL
# -42 -99 3 -110
#
# BITS (VERIFIED AGAINST CPYTHON)
# 0xd6 0b11010110
# 0x9d 0b10011101
# 0x03 0b00000011
# 0x92 0b10010010
