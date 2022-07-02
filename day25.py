from collections import deque
import numpy as np
import time

t = time.perf_counter()

with open("day25input.txt") as f:
    board = [x.strip() for x in f.readlines()]
for i in range(len(board)):
    board[i] = [x for x in board[i]]
board = np.array(board)

east = list()
south = list()
for iy, ix in np.ndindex(board.shape):
    if board[iy, ix] == '>':
        east.append([iy, ix])
    elif board[iy, ix] == 'v':
        south.append([iy, ix])

has_changed = True
steps = 0
queue = deque()
while has_changed:
    has_changed = False
    for i in range(len(east)):
        new_pos = [east[i][0], east[i][1] + 1]
        new_pos[1] %= len(board[0])
        if board[new_pos[0], new_pos[1]] == '.':
            queue.append((east[i][0], east[i][1], new_pos[0], new_pos[1]))   
            east[i][1] = new_pos[1]
            has_changed = True
    while len(queue) > 0:
        tmp = queue.pop()
        board[tmp[0], tmp[1]] = '.'
        board[tmp[2], tmp[3]] = '>'
    
    for i in range(len(south)):
        new_pos = [south[i][0] + 1, south[i][1]]
        new_pos[0] %= len(board)
        if board[new_pos[0], new_pos[1]] == '.':
            queue.append((south[i][0], south[i][1], new_pos[0], new_pos[1]))
            south[i][0] = new_pos[0]
            has_changed = True        
    while len(queue) > 0:
        tmp = queue.pop()
        board[tmp[0], tmp[1]] = '.'
        board[tmp[2], tmp[3]] = 'v'
    
    if has_changed:
        steps += 1

print("The first answer is:", steps+1)   
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")