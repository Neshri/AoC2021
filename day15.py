import numpy as np
from collections import deque

with open("day15input.txt") as f:
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
            
    #Down
    new_pos = (current_pos[0] + 1, current_pos[1])
    if current_pos[0] + 1 < len(board):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
          
    #Left
    new_pos = (current_pos[0], current_pos[1] - 1)
    if current_pos[1] - 1 > 0:
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            
    #Right
    new_pos = (current_pos[0], current_pos[1] + 1)
    if current_pos[1] + 1 < len(board[0]):
        if visits[new_pos] == 0:
            queue.append(new_pos)
            visits[new_pos] = 1
            board[new_pos] += board[current_pos]
        elif board[current_pos] + original_board[new_pos] < board[new_pos]:
            board[new_pos] = board[current_pos] + original_board[new_pos]
            
    

print("The first answer is:", board[(len(board) - 1, len(board[0]) - 1)])
print(board)
# for x in board:
#     print(list(x))