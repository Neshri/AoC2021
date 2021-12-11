import numpy as np
import time
t = time.perf_counter()

def charge(iy, ix, board, has_flashed):
    if iy < 0 or iy >= len(board) or ix < 0 or ix >= len(board[iy]):
        return
    if not has_flashed[iy, ix]:
        board[iy, ix] += 1
    if board[iy, ix] > 9:
        board[iy, ix] = 0
        has_flashed[iy, ix] += 1
        for new_iy, new_ix in np.ndindex((3, 3)):
            charge(iy + new_iy - 1, ix + new_ix - 1, board, has_flashed)
    return

def step(board):
    flash_count = 0
    has_flashed = np.zeros(board.shape)
    for iy, ix in np.ndindex(board.shape):
        charge(iy, ix, board, has_flashed)
    for iy, ix in np.ndindex(board.shape):
        if has_flashed[iy, ix] > 0:
            flash_count += 1
    return flash_count

with open("day11input.txt") as f:
    input = [x.strip() for x in f.readlines()]
for line in range(len(input)):
    input[line] = [int(x) for x in input[line]]
board = np.array(input)
flash_count = 0
for i in range(100):
    flash_count += step(board)
print("The first answer is:", flash_count)

board = np.array(input)
index = 0
super_flash = np.zeros(board.shape)
while True:
    step(board)
    index += 1
    if np.array_equal(board, super_flash):
        break
print("The second answer is:", index)
print("Execution time was:", int((time.perf_counter() - t) * 1000), "ms")