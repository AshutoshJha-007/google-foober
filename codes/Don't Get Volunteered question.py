def solution(src, dest):
    possible_moves = [(2, 1), (1, 2), (-1, 2), 
                    (2, -1), (-2, 1), (1, -2), 
                    (-1, -2), (-2, -1)]
    lines = [list(range(8*i, 8*i+8)) for i in range(0, 8)]
    next_moves = [src]
    moves_counter = 0
    while dest not in next_moves:
        all_moves = []
        for position in next_moves:
            idx = int(position/8), (position % 8)
            solutions = [(idx[0] + move[0], idx[1] + move [1]) for move in possible_moves\
                         if 0 <= idx[0] + move[0] < 8 and 0 <= idx[1]+ move[1] < 8]
            moves = [lines[coor[0]][coor[1]] for coor in solutions]
            all_moves += moves
        next_moves = all_moves
        moves_counter += 1
    return moves_counter