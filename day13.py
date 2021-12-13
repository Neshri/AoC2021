
def fold(axis, n, points):
    new_points = set()
    if axis == 'x':
        for point in points:
            if point[0] > n:
                distance = point[0] - n
                new_points.add((n - distance, point[1]))
            else:
                new_points.add(point)
    elif axis == 'y':
        for point in points:
            if point[1] > n:
                distance = point[1] - n
                new_points.add((point[0], n - distance))
            else:
                new_points.add(point)
    return new_points

with open("day13input.txt") as f:
    lines = f.readlines()
points = set()
folds = list()
for line in lines:
    line = line.strip()
    line = line.split(',')
    if len(line) <= 1:
        if "fold along" in line[0]:
            line = line[0].split()
            line = line[2].split('=')
            folds.append((line[0], int(line[1])))
    else:
        points.add((int(line[0]), int(line[1])))

ans = fold(folds[0][0], folds[0][1], points)
print("The first answer is:", len(ans))

for folding in folds:
    points = fold(folding[0], folding[1], points)

canvas = list()
ma = [0, 0]
for point in points:
    if point[0] > ma[0]:
        ma[0] = point[0]
    if point[1] > ma[1]:
        ma[1] = point[1]
ma[0] += 1
ma[1] += 1
for i in range(ma[1]):
    canvas.append(list(" " * ma[0]))

for point in points:
    canvas[point[1]][point[0]] = '#'

print("The second answer is:")
for i in canvas:
    print("".join(i))

