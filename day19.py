import numpy as np
import re
import math
import time
from collections import deque

from numpy.core.numeric import array_equal

t = time.perf_counter()


class scanner:
    def __init__(self, id, beacons) -> None:
        self.id = id
        self.beacons = beacons
        self.t_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        beacon_dists = dict()
        for i in range(len(beacons)):
            for j in range(i+1, len(beacons)):
                tmp = distance_squared(beacons[i], beacons[j])
                if tmp not in beacon_dists.keys():
                    beacon_dists[tmp] = set()
                l = min(beacons[i], beacons[j])
                r = max(beacons[i], beacons[j])
                beacon_dists[tmp].add((l, r))
        self.beacon_distances = beacon_dists
        

def distance_squared(p1, p2):
    tmp = (p1[0] - p2[0]) ** 2
    tmp += (p1[1] - p2[1]) ** 2
    tmp += (p1[2] - p2[2]) ** 2
    return tmp


def point_diff(p1, p2):
    p1 = np.array(p1, dtype='int64')
    p2 = np.array(p2, dtype='int64')
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2], 1)

def manhattan_point_diff(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def rotation_matrix(axis, degrees):
    rad = math.radians(degrees)
    if axis == 'x':
        return np.array([[1, 0, 0, 0], [0, math.cos(rad), -math.sin(rad), 0], [0, math.sin(rad), math.cos(rad), 0], [0, 0, 0, 1]], dtype="int64")
    elif axis == 'y':
        return np.array([[math.cos(rad), 0, math.sin(rad), 0], [0, 1, 0, 0], [-math.sin(rad), 0, math.cos(rad), 0], [0, 0, 0, 1]], dtype="int64")
    elif axis == 'z':
        return np.array([[math.cos(rad), -math.sin(rad), 0, 0], [math.sin(rad), math.cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="int64")

X_ROTATION = rotation_matrix('x', 90)
Y_ROTATION = rotation_matrix('y', 90)
Z_ROTATION = rotation_matrix('z', 90)

def rotation_matrix_a_to_b(a, b):
    rm = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="int64")
    if array_equal(np.dot(rm, a), b):
        return rm
    for x in range(4):
        for z in range(4):
            rm = np.dot(rm, Z_ROTATION)
            if array_equal(np.dot(rm, a), b):
                return rm
        rm = np.dot(rm, X_ROTATION)
        if array_equal(np.dot(rm, a), b):
            return rm
    rm = np.dot(rm, Y_ROTATION)
    if array_equal(np.dot(rm, a), b):
            return rm
    for z in range(4):
        rm = np.dot(rm, Z_ROTATION)
        if array_equal(np.dot(rm, a), b):
            return rm
    rm = np.dot(rm, Y_ROTATION)
    rm = np.dot(rm, Y_ROTATION)
    for z in range(4):
        if array_equal(np.dot(rm, a), b):
            return rm
        rm = np.dot(rm, Z_ROTATION)

    if not array_equal(np.dot(rm, a), b):
        print("Error:", a, "and", b, "axises could not be aligned. Trying next")
    return rm

# Read input
scanners = list()
with open("day19input.txt") as f:
    tmp = list()
    
    for line in f:
        line = line.strip()
        if re.fullmatch("--- scanner \d+ ---", line) != None:
            if len(tmp) > 0:
                scanners.append(tmp)
                tmp = list()
        elif line != '':
            line = line.split(',')
            tmp.append((int(line[0]), int(line[1]), int(line[2]), int(1)))
    if len(tmp) > 0:
        scanners.append(tmp)
for i in range(len(scanners)):
    scanners[i] = scanner(i, scanners[i])

# Prepare final box
beacons = set()
for x in scanners[0].beacons:
    beacons.add(tuple(x))
beacon_distances = dict()
tmp_list = list(beacons)
for i in range(len(beacons)):
    for j in range(i+1, len(beacons)):
        tmp = distance_squared(tmp_list[i], tmp_list[j])
        if tmp not in beacon_distances.keys():
            beacon_distances[tmp] = set()
        l = min(tmp_list[i], tmp_list[j])
        r = max(tmp_list[i], tmp_list[j])
        beacon_distances[tmp].add((l, r))

# Start adding scanners
queue = deque(scanners[1:])
while len(queue) > 0:
    current_scan = queue.popleft()
    overlap = 0
    equal_dists = list()
    for x in current_scan.beacon_distances.keys():
        if x in beacon_distances.keys():
            overlap += 1
            equal_dists.append(x)
    # 12 overlap -> 66 equal distances
    if overlap < 66:
        queue.append(current_scan)
    else:
        # POSSIBLE PROBLEM WITH DUPLICATE VALUES?!?!
        # Find corresponding points
        corresponding_p_dict = dict()
        for x in equal_dists:
            if len(beacon_distances[x]) > 1:
                print("Duplicate distances found in a")
            if len(current_scan.beacon_distances[x]) > 1:
                print("Duplicate distances found in b")
            a = next(iter(beacon_distances[x]))
            b = next(iter(current_scan.beacon_distances[x]))
            
            if b[0] not in corresponding_p_dict.keys():
                corresponding_p_dict[b[0]] = list(a)
            else:
                if type(corresponding_p_dict[b[0]]) is list:
                    if a[0] in corresponding_p_dict[b[0]]:
                        corresponding_p_dict[b[0]] = a[0]
                    elif a[1] in corresponding_p_dict[b[0]]:
                        corresponding_p_dict[b[0]] = a[1]

            if b[1] not in corresponding_p_dict.keys():
                corresponding_p_dict[b[1]] = list(a)
            else:
                if type(corresponding_p_dict[b[1]]) is list:
                    if a[0] in corresponding_p_dict[b[1]]:
                        corresponding_p_dict[b[1]] = a[0]
                    elif a[1] in corresponding_p_dict[b[1]]:
                        corresponding_p_dict[b[1]] = a[1]
        
        # Find transformation matrix
        a = list()
        b = list()
        for key in corresponding_p_dict.keys():
            if type(corresponding_p_dict[key]) is not list:
                a.append(list(key))
                b.append(list(corresponding_p_dict[key]))
        for i in range(len(a)-1):
            a_diff = np.array(point_diff(a[i], a[i+1]))
            b_diff = np.array(point_diff(b[i], b[i+1]))
            current_scan.t_matrix = rotation_matrix_a_to_b(a_diff, b_diff)
            if not np.array_equal(np.dot(current_scan.t_matrix, a_diff), b_diff):
                continue
            scanner_diff = point_diff(b[i], np.around(np.dot(current_scan.t_matrix, a[i]), decimals=0))
            current_scan.t_matrix[0][3] = scanner_diff[0]
            current_scan.t_matrix[1][3] = scanner_diff[1]
            current_scan.t_matrix[2][3] = scanner_diff[2]

        for x in range(len(a)):
            if not np.array_equal(np.dot(current_scan.t_matrix, a[x]), b[x]): 
                print("Error: point", a[x], "and", b[x], "does not correspond with eachother.")
               
        
        # add new beacons to final set
        for x in current_scan.beacons:
            tmp = tuple(np.around(np.dot(current_scan.t_matrix, np.array(x)), decimals=0))
            if tmp not in beacons:
                for b in beacons:
                    distance = distance_squared(tmp, b)
                    if distance not in beacon_distances.keys():
                        beacon_distances[distance] = set()
                    l = min(tmp, b)
                    r = max(tmp, b)
                    beacon_distances[distance].add((l, r))
            beacons.add(tmp)
        
print("The first answer is:", len(beacons))
# Part 2
scanner_positions = list()
for s in scanners:
    m = s.t_matrix
    scanner_positions.append((m[0][3], m[1][3], m[2][3]))
ans = 0
for i in range(len(scanner_positions)):
    for j in range(i+1, len(scanner_positions)):
        man_dist = manhattan_point_diff(scanner_positions[i], scanner_positions[j])
        if man_dist > ans:
            ans = man_dist
print("The second answer is:", ans)
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")