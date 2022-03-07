import numpy as np
from collections import deque
import time
t = time.perf_counter()
AMPHIPOD_DESTINATIONS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
AMPHIPOD_TYPES = set(['A', 'B', 'C', 'D'])
AMPHIPOD_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}




def move(old_y, old_x, new_y, new_x, board):
    cost = 0
    letter = board[old_y][old_x]
    # Trying to move non-amphipod
    if letter not in AMPHIPOD_TYPES:
        return False, cost
    # Destination occupied?
    if board[new_y][new_x] != '.':
        return False, cost
    # Room has incorrect occupant?
    if new_x == AMPHIPOD_DESTINATIONS[letter]:
        tmp = set(('.', 'x', '#', letter))
        for y_i in range(len(board)):
            if board[y_i][new_x] not in tmp:
                return False, cost
    # Start moving
    pos = [old_y, old_x]
    while pos[0] != new_y or pos[1] != new_x:
        if pos[1] == new_x:
            y_dir = 1 if pos[0] < new_y else -1
            if board[pos[0] + y_dir][pos[1]] == '.' or board[pos[0] + y_dir][pos[1]] == 'x':
                pos[0] += 1
                cost += 1
            else:
                return False, cost
        else:
            x_dir = 1 if pos[1] < new_x else -1
            if board[pos[0]][pos[1] + x_dir] == '.' or board[pos[0]][pos[1] + x_dir] == 'x':
                pos[1] += x_dir
                cost += 1
            elif board[pos[0] - 1][pos[1]] == '.' or board[pos[0] - 1][pos[1]] == 'x':
                pos[0] -= 1
                cost += 1
            else:
                return False, cost
    return True, cost * AMPHIPOD_COSTS[letter]


def board_hash(a):
    h = 0
    for y in range(len(a)):
        h += hash(tuple(a[y])) * y
    return h


def find_cheapest(from_board, to_board):
    HALLWAY = list()
    ROOMS = list()
    AMPHIPOD_DESTINATIONS = {'A': list(), 'B': list(), 'C': list(), 'D': list()}
    for y in range(len(to_board)):
        for x in range(len(to_board[y])):
            if to_board[y, x] in AMPHIPOD_DESTINATIONS.keys():
                AMPHIPOD_DESTINATIONS[to_board[y, x]].insert(0, (y, x))
                ROOMS.append((y, x))
            elif to_board[y, x] == '.':
                HALLWAY.append((y, x))
    
    queue = deque()
    FINISHED_HASH = board_hash(to_board)
    state_costs = dict()
    queue.append(from_board)
    processed = set()
    while len(queue) > 0:
        state = queue.pop()
        state_hash = board_hash(state)
        if state_hash in processed or state_hash == FINISHED_HASH:
            continue

        has_moved = False
        for old_point in HALLWAY:
            if state[old_point] in AMPHIPOD_TYPES:
                for new_point in AMPHIPOD_DESTINATIONS[state[old_point]]:
                    if state[new_point] != state[old_point] and state[new_point] != '.':
                        break
                    moveable, cost = move(old_point[0], old_point[1], new_point[0], new_point[1], state)
                    if moveable:
                        update_queue(queue, state_costs, state, state_hash, old_point, new_point, cost)
                        has_moved = True
                        break
            if has_moved:
                break
        if has_moved:
            continue
        for old_point in ROOMS:
            if state[old_point] in AMPHIPOD_TYPES:
                if old_point in AMPHIPOD_DESTINATIONS[state[old_point]]:
                    incorrect_occupants = False
                    for p in AMPHIPOD_DESTINATIONS[state[old_point]]:
                        if p == old_point:
                            break
                        if state[p] != state[old_point]:
                            incorrect_occupants = True
                            break
                    if not incorrect_occupants:
                        continue
                for new_point in AMPHIPOD_DESTINATIONS[state[old_point]]:
                    if old_point == new_point:
                        continue
                    if state[new_point] != state[old_point] and state[new_point] != '.':
                        break
                    moveable, cost = move(old_point[0], old_point[1], new_point[0], new_point[1], state)
                    if moveable:
                        update_queue(queue, state_costs, state, state_hash, old_point, new_point, cost)
                        has_moved = True
                        break
                if not has_moved:
                    for new_point in HALLWAY:
                        moveable, cost = move(old_point[0], old_point[1], new_point[0], new_point[1], state)
                        if moveable:
                            update_queue(queue, state_costs, state, state_hash, old_point, new_point, cost)
                else:
                    break
        processed.add(state_hash)
    # Calculate cheap path
    cheapest = 2 ** 63
    queue = deque()
    queue.append((0, FINISHED_HASH))
    first_hash = board_hash(from_board)
    while len(queue) > 0:
        cost, current_hash = queue.pop()
        if current_hash == first_hash:
            if cost < cheapest:
                cheapest = cost
        else:
            for a in state_costs[current_hash]:
                queue.append((cost + a[0], a[1]))
    return cheapest

def update_queue(queue, state_costs, state, state_hash, old_point, new_point, cost):
    new_state = np.array(state, copy=True)
    new_state[old_point] = '.'
    new_state[new_point] = state[old_point]
    new_hash = board_hash(new_state)
    if new_hash not in state_costs.keys():
        state_costs[new_hash] = set()
    if (cost, state_hash) not in state_costs[new_hash]:
        state_costs[new_hash].add((cost, state_hash))
        queue.append(new_state)


with open("day23input.txt") as f:
    board = [list(x.replace('\n', '')) for x in f.readlines()]
for b in board:
    for i in range(len(board[0]) - len(b)):
        b.append(' ')
board = np.array(board)
rooms = (3, 5, 7, 9)
for r in rooms:
    board[1, r] = 'x'

finished_board = np.array(board, copy=True)
for y_i in range(2, 4):
    finished_board[y_i][3] = 'A'
    finished_board[y_i][5] = 'B'
    finished_board[y_i][7] = 'C'
    finished_board[y_i][9] = 'D'

ans = find_cheapest(board, finished_board)
print("The first answer is:", ans)

print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")

board = np.insert(board, 3, list("  #D#B#A#C#  "), axis=0)
board = np.insert(board, 3, list("  #D#C#B#A#  "), axis=0)
finished_board = np.array(board, copy=True)
for y_i in range(2, 6):
    finished_board[y_i][3] = 'A'
    finished_board[y_i][5] = 'B'
    finished_board[y_i][7] = 'C'
    finished_board[y_i][9] = 'D'

print("The second answer is:", find_cheapest(board, finished_board))
print("The total execution time was:", int((time.perf_counter() - t) * 1000), "ms")
