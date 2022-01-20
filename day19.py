import numpy as np
import re
import math
import time
from collections import deque

t = time.perf_counter()


class scanner:

    def __init__(self, id, beacons) -> None:
        self.id = id
        self.beacons = beacons
        self.t_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        beacon_dists = dict()
        for i in range(len(beacons)):
            for j in range(i+1, len(beacons)):
                tmp = get_squared_distance(beacons[i], beacons[j])
                if tmp not in beacon_dists.keys():
                    beacon_dists[tmp] = set()
                l = min(beacons[i], beacons[j])
                r = max(beacons[i], beacons[j])
                beacon_dists[tmp].add((l, r))
        self.beacon_distances = beacon_dists
        

def get_squared_distance(p1, p2):
    tmp = (p1[0] - p2[0]) ** 2
    tmp += (p1[1] - p2[1]) ** 2
    tmp += (p1[2] - p2[2]) ** 2
    return tmp
    

def rotation_matrix(axis, degrees):
    rad = math.radians(degrees)
    if axis == 'x':
        return np.around(np.array([[1, 0, 0, 0], [0, math.cos(rad), -math.sin(rad), 0], [0, math.sin(rad), math.cos(rad), 0], [0, 0, 0, 1]]), decimals=0)
    elif axis == 'y':
        return np.around(np.array([[math.cos(rad), 0, math.sin(rad), 0], [0, 1, 0, 0], [-math.sin(rad), 0, math.cos(rad), 0], [0, 0, 0, 1]]), decimals=0)
    elif axis == 'z':
        return np.around(np.array([[math.cos(rad), -math.sin(rad), 0, 0], [math.sin(rad), math.cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), decimals=0)

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
        tmp = get_squared_distance(tmp_list[i], tmp_list[j])
        if tmp not in beacon_distances.keys():
            beacon_distances[tmp] = set()
        l = min(tmp_list[i], tmp_list[j])
        r = max(tmp_list[i], tmp_list[j])
        beacon_distances[tmp].add((l, r))

# Start adding scanners
queue = deque()
for x in scanners[1:]:
    queue.append(x)
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
        
        break


print("The first answer is:", len(beacons))

print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")