def solution(x, y):
    line = x + y - 1
    start_line = sum(range(line))
    worker_id = str(start_line + x)
    return worker_id
