# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 12:31:52 2021

@author: AntonLundgren
"""
import time
import numpy as np
t = time.perf_counter()

def check_if_low(x, y, matrix):
    if y - 1 >= 0 and matrix[y][x] >= matrix[y-1][x]:
        return False
    if y + 1 < len(matrix) and matrix[y][x] >= matrix[y+1][x]:
        return False
    if x - 1 >= 0 and matrix[y][x] >= matrix[y][x-1]:
        return False
    if x + 1 < len(matrix[y]) and matrix[y][x] >= matrix[y][x+1]:
        return False

    return True

# Wriggle through the matrix
def wriggle(x, y, matrix, visit_set, low_points):
    wrigglesum = 0
    if (x, y) in visit_set or matrix[y][x] == 9:
        return wrigglesum
    else:
        wrigglesum += 1
        visit_set.add((x, y))
        if (x, y) in low_points:
            low_points.remove((x, y))
    # Up
    new_x, new_y = x, y
    new_y -= 1
    while new_y >= 0:
        tmp = wriggle(new_x, new_y, matrix, visit_set, low_points)
        if tmp == 0:
            break
        wrigglesum += tmp
        new_y -= 1

    # Down
    new_x, new_y = x, y
    new_y += 1
    while new_y < len(matrix):
        tmp = wriggle(new_x, new_y, matrix, visit_set, low_points)
        if tmp == 0:
            break
        wrigglesum += tmp
        new_y += 1

    # Left
    new_x, new_y = x, y
    new_x -= 1
    while new_x >= 0:
        tmp = wriggle(new_x, new_y, matrix, visit_set, low_points)
        if tmp == 0:
            break
        wrigglesum += tmp
        new_x -= 1

    # Right
    new_x, new_y = x, y
    new_x += 1
    while new_x < len(matrix[y]):
        tmp = wriggle(new_x, new_y, matrix, visit_set, low_points)
        if tmp == 0:
            break
        wrigglesum += tmp
        new_x += 1

    return wrigglesum


with open("day9input.txt") as f:
    data = [x.strip() for x in f.readlines()]
for i in range(len(data)):
    data[i] = [int(x) for x in data[i]]
data = np.array(data)

low_points = []
count = 0
for y in range(len(data)):
    for x in range(len(data[y])):
        if check_if_low(x, y, data):
            count += (data[y][x] + 1)
            low_points.append((x, y))
print("The first answer is:", count)
points_to_check = set(low_points)
basins = []
while len(points_to_check) > 0:
    point = points_to_check.pop()
    basins.append(wriggle(point[0], point[1], data, set(), points_to_check))

basins = sorted(basins, reverse=True)
count = basins[0] * basins[1] * basins[2]
print("The second answer is:", count)
print("Execution time:", int((time.perf_counter() - t)*1000), "ms")
