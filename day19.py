import numpy as np
import re
import math
import time

t = time.perf_counter()


class scanner:

    def __init__(self, id, beacons) -> None:
        self.id = id
        self.beacons = beacons
        self.t_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        
        tmp_list = list()
        for i in range(len(beacons)):
            for j in range(i+1, len(beacons)):
                tmp = (beacons[i][0] - beacons[j][0]) ** 2
                tmp += (beacons[i][1] - beacons[j][1]) ** 2
                tmp += (beacons[i][2] - beacons[j][2]) ** 2
                tmp_list.append((tmp, i, j))
        tmp_list.sort()
        self.beacon_distances = tmp_list
        


    


def rotation_matrix(axis, degrees):
    rad = math.radians(degrees)
    if axis == 'x':
        return np.around(np.array([[1, 0, 0, 0], [0, math.cos(rad), -math.sin(rad), 0], [0, math.sin(rad), math.cos(rad), 0], [0, 0, 0, 1]]), decimals=0)
    elif axis == 'y':
        return np.around(np.array([[math.cos(rad), 0, math.sin(rad), 0], [0, 1, 0, 0], [-math.sin(rad), 0, math.cos(rad), 0], [0, 0, 0, 1]]), decimals=0)
    elif axis == 'z':
        return np.around(np.array([[math.cos(rad), -math.sin(rad), 0, 0], [math.sin(rad), math.cos(rad), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), decimals=0)


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
    scanners[i] = scanner(i, np.array(scanners[i]))

beacons = set()
for x in scanners[0].beacons:
    beacons.add((x[0], x[1], x[2]))



# 12 overlap -> 66 equal distances
print("The first answer is:", len(beacons))

print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")