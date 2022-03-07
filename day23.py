import numpy as np
from collections import deque
AMPHIPOD_DESTINATIONS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
AMPHIPOD_TYPES = set(['A', 'B', 'C', 'D'])
HALLWAY = (1, 2, 4, 6, 8, 10, 11)
ROOMS = (3, 5, 7, 9)
AMPHIPOD_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}




def move(old_y, old_x, new_y, new_x, board):
    cost = 0
    letter = board[old_y][old_x]
    if board[new_y][new_x] != '.':
        return False, cost
    if new_x == AMPHIPOD_DESTINATIONS[letter] and new_y == 2 and board[3][new_x] != letter:
        return False, cost
    if old_x == AMPHIPOD_DESTINATIONS[letter]:
        return False, cost
    if letter not in AMPHIPOD_TYPES:
        return False, cost
    
    pos = [old_y, old_x]
    while pos[0] != new_y or pos[1] != new_x:
        if pos[1] == new_x:
            if board[pos[0] + 1][pos[1]] == '.' or board[pos[0] + 1][pos[1]] == 'x':
                pos[0] += 1
                cost += 1
            else:
                return False, cost
        else:
            x_dir = (new_x - old_x) // abs(new_x - old_x)
            if board[pos[0]][pos[1] + x_dir] == '.' or board[pos[0]][pos[1] + x_dir] == 'x':
                pos[1] += x_dir
                cost += 1
            elif board[pos[0] - 1][pos[1]] == '.' or board[pos[0] - 1][pos[1]] == 'x':
                pos[0] += -1
                cost += 1
            else:
                return False, cost
    return True, cost * AMPHIPOD_COSTS[letter]




def board_copy(board):
    copy = list()
    for y in board:
        tmp = list()
        for x in y:
            tmp.append(x)
        copy.append(tmp)
    return np.array(copy)

def equal_matrix(a, b):
    for y in range(len(a)):
        for x in range(len(a[y])):
            if a[y][x] != b[y][x]:
                return False
    return True

def board_hash(a):
    h = 0
    for y in range(len(a)):
        h += hash(tuple(a[y])) * y
    return h

def print_board(a):
    for y in a:
        print(y)




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
        if state_hash in processed:
            continue
        for h_point in HALLWAY:
            if state[h_point] in AMPHIPOD_TYPES:
                for dest in AMPHIPOD_DESTINATIONS[state[h_point]]:
                    if state[dest] != state[h_point] and state[dest] != '.':
                        break
                    moveable, cost = move(h_point[0], h_point[1], dest[0], dest[1], state)
                    if moveable:
                        new_state = np.array(state, copy=True)
                        new_state[h_point] = '.'
                        new_state[dest] = state[h_point]
                        new_hash = board_hash(new_state)
                        if new_hash not in state_costs.keys():
                            state_costs[new_hash] = list()
                        state_costs[new_hash].append(cost, state_hash)
                        queue.append(new_state)
        
        for r_point in ROOMS:
            if state[r_point] in AMPHIPOD_TYPES:

                pass

        processed.add(state_hash)
    return 0


with open("day23input.txt") as f:
    board = [list(x.replace('\n', '')) for x in f.readlines()]
for b in board:
    for i in range(len(board[0]) - len(b)):
        b.append(' ')
board = np.array(board)
for r in ROOMS:
    board[1, r] = 'x'
cheapest_cost = 2 ** 63

FINISHED_BOARD = np.array(board, copy=True)
FINISHED_BOARD[2][3] = FINISHED_BOARD[3][3] = 'A'
FINISHED_BOARD[2][5] = FINISHED_BOARD[3][5] = 'B'
FINISHED_BOARD[2][7] = FINISHED_BOARD[3][7] = 'C'
FINISHED_BOARD[2][9] = FINISHED_BOARD[3][9] = 'D'

ans = find_cheapest(board, FINISHED_BOARD)
print(ans)
# queue.append((board, 0))
# def move_hallway(AMPHIPOD_DESTINATIONS, AMPHIPOD_TYPES, HALLWAY, move, board_copy, queue, state):
#     for x in HALLWAY:
#         l = state[0][1][x]
#         old_pos = (1, x)
#         if l in AMPHIPOD_TYPES:
#             new_pos = (3, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 # cost = 2 + abs(x - AMPHIPOD_DESTINATIONS[l])
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#             new_pos = (2, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#     return False

# def move_rooms(AMPHIPOD_DESTINATIONS, AMPHIPOD_TYPES, HALLWAY, ROOMS, move, board_copy, queue, state):
#     for x in ROOMS:
#         l = state[0][2][x]
#         old_pos = (2, x)
#         if l in AMPHIPOD_TYPES:
#             new_pos = (3, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#             new_pos = (2, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#             for x_i in HALLWAY:
#                 new_pos = (1, x_i)
#                 moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#                 if moveable:
#                     c = board_copy(state[0])
#                     c[old_pos[0]][old_pos[1]] = '.'
#                     c[new_pos[0]][new_pos[1]] = l
#                     queue.append((c, state[1] + cost))
#         l = state[0][3][x]
#         old_pos = (3, x)
#         if l in AMPHIPOD_TYPES:
#             new_pos = (3, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#             new_pos = (2, AMPHIPOD_DESTINATIONS[l])
#             moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#             if moveable:
#                 c = board_copy(state[0])
#                 c[old_pos[0]][old_pos[1]] = '.'
#                 c[new_pos[0]][new_pos[1]] = l
#                 queue.append((c, state[1] + cost))
#                 return True
#             for x_i in HALLWAY:
#                 new_pos = (1, x_i)
#                 moveable, cost = move(old_pos[0], old_pos[1], new_pos[0], new_pos[1], state[0])
#                 if moveable:
#                     c = board_copy(state[0])
#                     c[old_pos[0]][old_pos[1]] = '.'
#                     c[new_pos[0]][new_pos[1]] = l
#                     queue.append((c, state[1] + cost))
#     return False
# processed = dict()
# while len(queue) > 0:
#     state = queue.pop()
#     hash_state = board_hash(state[0])
#     if hash_state in processed:
#         if state[1] < processed[hash_state]:
#             processed[hash_state] = state[1]
#         continue
#     if equal_matrix(state[0], FINISHED_BOARD):
#         print(len(queue), cheapest_cost)
#         # print_board(state[0])
#         if state[1] < cheapest_cost:
#             cheapest_cost = state[1]
#             continue
#     # Check Hallway
#     if not move_hallway(AMPHIPOD_DESTINATIONS, AMPHIPOD_TYPES, HALLWAY, move, board_copy, queue, state):
#         # Check Rooms
#         move_rooms(AMPHIPOD_DESTINATIONS, AMPHIPOD_TYPES, HALLWAY, ROOMS, move, board_copy, queue, state)
#         # print_board(state[0])
#     processed[hash_state] = state[1]
# h = board_hash(FINISHED_BOARD)
# print(processed[h])
# print("The first answer is:", cheapest_cost)
