import numpy as np
import time
t = time.perf_counter()

# calculate the binary value of 3*3 square using the default for out of bounds values
# could optimize by checking if x, y is missing entry but is inside the boundary then 0
def box_binary(y, x, image, default):
    send = 0
    for y_i in range(y-1, y+2):
        for x_i in range(x-1, x+2):
            if (y_i, x_i) in image.keys():
                if image[(y_i, x_i)] == 1:
                    send += 1
            else:
                send += default
            send <<= 1
    send >>= 1
    return send

# Enhance image once with out of bounds set to the default value
def enhance(in_image, filter, default):
    y_range = [0, 0]
    x_range = [0, 0]
    for key in in_image.keys():
        y_range[0] = min(key[0], y_range[0])
        y_range[1] = max(key[0], y_range[1])
        x_range[0] = min(key[1], x_range[0])
        x_range[1] = max(key[1], x_range[1])
    binary_board = dict()
    for y_i in range(y_range[0], y_range[1]+1):
        for x_i in range(x_range[0], x_range[1]+1):
            binary_board[(y_i, x_i)] = box_binary(y_i, x_i, in_image, default)
    repeating_value = 0
    has_changed = True
    while has_changed:
        has_changed = False
        y_range[0] -= 1
        y_range[1] += 1
        x_range[0] -= 1
        x_range[1] += 1
        repeating_value = box_binary(y_range[0], x_range[0], in_image, default)
        for x_i in range(x_range[0], x_range[1]+1):
            tmp = box_binary(y_range[0], x_i, in_image, default)
            binary_board[(y_range[0], x_i)] = tmp
            if tmp != repeating_value:
                has_changed = True
            tmp = box_binary(y_range[1], x_i, in_image, default)
            binary_board[(y_range[1], x_i)] = tmp
            if tmp != repeating_value:
                has_changed = True
        for y_i in range(y_range[0], y_range[1]+1):
            tmp = box_binary(y_i, x_range[0], in_image, default)
            binary_board[(y_i, x_range[0])] = tmp
            if tmp != repeating_value:
                has_changed = True
            tmp = box_binary(y_i, x_range[1], in_image, default)
            binary_board[(y_i, x_range[1])] = tmp
            if tmp != repeating_value:
                has_changed = True
    out_image = dict()
    for key in binary_board.keys():
        out_image[key] = filter[binary_board[key]]
        out_image[key] = 1 if out_image[key] == '#' else 0
    repeating_value = 1 if filter[repeating_value] == '#' else 0
    return out_image, repeating_value


# Read and arrange the input
with open("day20input.txt") as f:
    iea = f.readline().strip()
    f.readline()
    in_image = [x.strip() for x in f.readlines()]
board = dict()
for y_i in range(len(in_image)):
    for x_i in range(len(in_image[0])):
        board[(y_i, x_i)] = 1 if in_image[y_i][x_i] == '#' else 0

# Enhance 2 times
default = 0
for i in range(2):
    board, default = enhance(board, iea, default)

# Create full image
y_range = [0, 0]
x_range = [0, 0]
for key in board.keys():
    y_range[0] = min(key[0], y_range[0])
    y_range[1] = max(key[0], y_range[1])
    x_range[0] = min(key[1], x_range[0])
    x_range[1] = max(key[1], x_range[1])
enhanced_image = np.full(shape=(x_range[1] - x_range[0], y_range[1] - y_range[0]), fill_value='#')
for key in board.keys():
    enhanced_image[key[1], key[0]] = '.' if board[key] == 0 else '#'

# Count the lights
ans = 0
for point in np.nditer(enhanced_image):
    if point == '#':
        ans += 1
print("The first answer is:", ans)

# Enhance 48 times more for a total of 50
for i in range(48):
    board, default = enhance(board, iea, default)


# Create full image
y_range = [0, 0]
x_range = [0, 0]
for key in board.keys():
    y_range[0] = min(key[0], y_range[0])
    y_range[1] = max(key[0], y_range[1])
    x_range[0] = min(key[1], x_range[0])
    x_range[1] = max(key[1], x_range[1])
enhanced_image = np.full(shape=(x_range[1] - x_range[0], y_range[1] - y_range[0]), fill_value='#')
for key in board.keys():
    enhanced_image[key[1], key[0]] = '.' if board[key] == 0 else '#'

# Print for fun
with open("output.txt", "w") as f:
    f.writelines([''.join(line)+'\n' for line in enhanced_image])

# Count the lights
ans = 0
for point in np.nditer(enhanced_image):
    if point == '#':
        ans += 1
print("The second answer is:", ans)
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")