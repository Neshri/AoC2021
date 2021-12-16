import numpy as np
from collections import deque
import time
t = time.perf_counter()


def calculate_cheapest_path(board):
    def visit_and_check(current_pos, adjacent_pos):
        if visits[adjacent_pos] == 0:
            queue.append(adjacent_pos)
            visits[adjacent_pos] = 1
            board[adjacent_pos] += board[current_pos]
        elif board[current_pos] + original_board[adjacent_pos] < board[adjacent_pos]:
            board[adjacent_pos] = board[current_pos] + original_board[adjacent_pos]
            queue.append(adjacent_pos)
    
    original_board = np.array(board, copy=True)
    board = np.array(board, copy=True)
    visits = np.zeros(board.shape)
    visits[(0, 0)] = 1
    board[(0, 0)] = 0
    queue = deque()
    queue.append((0, 0))
    print_set = set()
    while len(queue) > 0:
        current_pos = queue.popleft()
        if current_pos not in print_set and current_pos[0] == current_pos[1]:
            print(current_pos)
            print_set.add(current_pos)
        #Up
        adjacent_pos = (current_pos[0] - 1, current_pos[1])
        if current_pos[0] - 1 >= 0:
            visit_and_check(current_pos, adjacent_pos)      
        #Down
        adjacent_pos = (current_pos[0] + 1, current_pos[1])
        if current_pos[0] + 1 < len(board):
            visit_and_check(current_pos, adjacent_pos)
        #Left
        adjacent_pos = (current_pos[0], current_pos[1] - 1)
        if current_pos[1] - 1 >= 0:
            visit_and_check(current_pos, adjacent_pos)    
        #Right
        adjacent_pos = (current_pos[0], current_pos[1] + 1)
        if current_pos[1] + 1 < len(board[0]):
            visit_and_check(current_pos, adjacent_pos)
    
    return board


with open("day15input.txt") as f:
    board = [x.strip() for x in f.readlines()]
for i in range(len(board)):
    board[i] = [int(x) for x in board[i]]
original_board = np.array(board, copy=True)
board = np.array(board, copy=True)

        
board = calculate_cheapest_path(board)
# print(board)
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

board = calculate_cheapest_path(board)
print("The second answer is:", board[(len(board) - 1, len(board[0]) - 1)])


print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")