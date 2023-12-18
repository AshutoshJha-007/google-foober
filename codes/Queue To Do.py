def solution(start, length):
    checksum = 0
    cur = start
    cur_len = length
    while cur_len > 0:
        checksum ^= xorsum(cur) ^ xorsum(cur + cur_len)
        cur += length
        cur_len -= 1
    return checksum
def xorsum(n):
    if n == 0:
        return 0
    remainder = (n - 1) % 4
    if remainder == 0:
        return n - 1
    elif remainder == 1:
        return 1
    elif remainder == 2:
        return n
    else:
        return 0