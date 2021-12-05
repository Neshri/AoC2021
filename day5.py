# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 18:32:56 2021

@author: AntonLundgren
"""
import numpy as np
import time
t = time.perf_counter()

with open("day5input.txt") as f:
    vectors = [x.strip().split("->") for x in f.readlines()]
for x in range(len(vectors)):
    tmp = vectors[x][0].strip().split(',')
    tmp.extend(vectors[x][1].strip().split(','))
    vectors[x] = [int(y) for y in tmp]
    
vectors = np.array(vectors)
board = np.zeros((1000, 1000), dtype=int)
for (x1, y1, x2, y2) in vectors:
    mi = (min(x1, x2), min(y1, y2))
    ma = (max(x1, x2), max(y1, y2))
    if x1 == x2 or y1 == y2:
        board[mi[0]:ma[0]+1, mi[1]:ma[1]+1] += 1

count = 0
for x, y in np.ndindex(board.shape):
    if board[x, y] > 1:
        count += 1
print("The first answer is: ", count)

for (x1, y1, x2, y2) in vectors:
    if x1 != x2 and y1 != y2:
        direction = [x2 - x1, y2 - y1]
        direction = np.sign(direction)
        board[x2, y2] += 1
        while x1 != x2:
            board[x1, y1] += 1
            x1 += direction[0]
            y1 += direction[1]
        

count = 0
for x, y in np.ndindex(board.shape):
    if board[x, y] > 1:
        count += 1
print("The second answer is: ", count)
print("Execution time:", int((time.perf_counter()-t)*1000), "ms")