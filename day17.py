import re

def is_in_zone(x, y):
    if x < x_min or x > x_max:
        return False
    if y < y_min or y > y_max:
        return False
    return True

def passes_zone(dx, dy):
    if dx * (dx + 1) // 2 < x_min or dx > x_max:
        return False
    if abs(dy) > max(abs(y_max), abs(y_min)):
        return False
    x = 0
    y = 0
    while True:
        x += dx
        y += dy
        dx = max(dx - 1, 0)
        dy -= 1 
        if is_in_zone(x, y):
            return True
        if x > x_max or y < y_min:
            return False
    

with open("day17input.txt") as f:
    x_min, x_max, y_min, y_max = [int(x) for x in re.findall("-?\d+" ,f.readline().strip())]

max_dy = max(abs(y_min), abs(y_max)) - 1
max_height = max_dy * (max_dy + 1) // 2
print("The first answer is:", max_height)

distinct_counter = 0
for dx in range(x_max+1):
    for dy in range(y_min, max_dy+1):
        if passes_zone(dx, dy):
            distinct_counter += 1
print("The second answer is:", distinct_counter)