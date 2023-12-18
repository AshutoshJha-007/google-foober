def solution(x, y):
    symmetric_diff = list(set(x) ^ set(y))
    result = symmetric_diff[0]
    return result