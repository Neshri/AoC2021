import numpy as np
from collections import deque
import time
t = time.perf_counter()

with open("testinput.txt") as f:
    board = [x.strip() for x in f.readlines()]
for i in range(len(board)):
    board[i] = [int(x) for x in board[i]]
original_board = np.array(board)
board = np.array(board)
visits = np.zeros(board.shape)
visits[(0, 0)] = 1
board[(0, 0)] = 0
queue = deque()
queue.append((0, 0))

while len(queue) > 0:
    current_pos = queue.popleft()
    #Up
    new_pos = (current_pos[0] - 1, current_pos[1])
    if current_pos[0] - 1 > 0:
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
            
    #Down
    new_pos = (current_pos[0] + 1, current_pos[1])
    if current_pos[0] + 1 < len(board):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
          
    #Left
    new_pos = (current_pos[0], current_pos[1] - 1)
    if current_pos[1] - 1 > 0:
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
            
    #Right
    new_pos = (current_pos[0], current_pos[1] + 1)
    if current_pos[1] + 1 < len(board[0]):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
            
    

print("The first answer is:", board[(len(board) - 1, len(board[0]) - 1)])

board = np.zeros((len(board) * 5, len(board[0]) * 5), dtype="int64")
for iy, ix in np.ndindex(board.shape):
    tmp = (iy // len(original_board)) + (ix // len(original_board[0]))
    board[iy, ix] = original_board[iy % len(original_board), ix % len(original_board[0])]
    board[iy, ix] += tmp
    tmp = board[iy, ix] // 10
    board[iy, ix] += tmp
    board[iy, ix] = board[iy, ix] % 10
    
original_board = np.array(board, copy=True)

visits = np.zeros(board.shape)
visits[(0, 0)] = 1
board[(0, 0)] = 0
queue = deque()
queue.append((0, 0))
print_set = set()

while len(queue) > 0:
    current_pos = queue.popleft()
    if current_pos not in print_set and current_pos[0] == current_pos[1]:
        print_set.add(current_pos)
        print(current_pos)
    #Up
    new_pos = (current_pos[0] - 1, current_pos[1])
    if current_pos[0] - 1 > 0:
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
            
    #Down
    new_pos = (current_pos[0] + 1, current_pos[1])
    if current_pos[0] + 1 < len(board):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
          
    #Left
    new_pos = (current_pos[0], current_pos[1] - 1)
    if current_pos[1] - 1 > 0:
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)
            
    #Right
    new_pos = (current_pos[0], current_pos[1] + 1)
    if current_pos[1] + 1 < len(board[0]):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            queue.append(new_pos)

# for x in original_board:
#     print(x)
print("The second answer is:", board[(len(board) - 1, len(board[0]) - 1)])


print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")