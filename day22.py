import re
import time

t = time.perf_counter()

def volume(bound_x, bound_y, bound_z):
    dx = bound_x[1] - bound_x[0] + 1
    dy = bound_y[1] - bound_y[0] + 1
    dz = bound_z[1] - bound_z[0] + 1
    return dx * dy * dz

def overlap(a, b):
    if a[1] < b[0] or a[0] > b[1]:
        return False
    else:
        return True

def volume_overlap(x1, y1, z1, x2, y2, z2):
    if not crosses(x1, y1, z1, x2, y2, z2):
        return None
    x = list(x1)
    x.extend(x2)
    x.sort()
    y = list(y1)
    y.extend(y2)
    y.sort()
    z = list(z1)
    z.extend(z2)
    z.sort()
    xyz = ((x[1], x[2]), (y[1], y[2]), (z[1], z[2]))
    return xyz

def crosses(x1, y1, z1, x2, y2, z2):
    if overlap(x1, x2) and overlap(y1, y2) and overlap(z1, z2):
        return True
    return False


with open("day22input.txt") as f:
    instructions = [x.strip() for x in f.readlines()]
for i in range(len(instructions)):
    setting, coords = instructions[i].split(' ')
    x, y, z = coords.split(',')
    x = re.findall("-*\d+", x)
    x = (int(x[0]), int(x[1]))
    y = re.findall("-*\d+", y)
    y = (int(y[0]), int(y[1]))
    z = re.findall("-*\d+", z)
    z = (int(z[0]), int(z[1]))
    instructions[i] = (setting, x, y, z)

volumes = list()
for instr in instructions:
    setting = instr[0]
    x = instr[1]
    y = instr[2]
    z = instr[3]   
    vol = volume(x, y, z)
    overlaps = list()
    for v in volumes:
        tmp = volume_overlap(x, y, z, v[0], v[1], v[2])
        if tmp != None:
            sign = -1 if v[3] > 0 else 1
            overlaps.append((tmp[0], tmp[1], tmp[2], sign * volume(tmp[0], tmp[1], tmp[2])))
    volumes.extend(overlaps)
    if setting == "on":
        volumes.append((x, y, z, vol))

init_region = ((-50, 50), (-50, 50), (-50, 50))
ans = 0
for v in volumes:
    tmp = volume_overlap(init_region[0], init_region[1], init_region[2], v[0], v[1], v[2])
    if tmp != None:
        sign = -1 if v[3] < 0 else 1
        ans += sign * volume(tmp[0], tmp[1], tmp[2])
print("The first answer is:", ans)
ans = 0
for v in volumes:
    ans += v[3]
print("The second answer is:", ans)
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")