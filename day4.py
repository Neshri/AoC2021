# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 15:52:27 2021

@author: AntonLundgren
"""
import time
t = time.perf_counter()
board_size = 5


def mark_board(number, board, check_board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if number == board[y][x]:
                check_board[y][x] = True
    
    return check_board

def has_bingo(check_board):
    #Horizontal check
    for y in range(len(check_board)):
        bingo = True
        for x in range(len(check_board[0])):
            if not check_board[y][x]:
                bingo = False
                break
        if bingo:
            return True
    #Vertical check
    for x in range(len(check_board[0])):
        bingo = True
        for y in range(len(check_board)):
            if not check_board[y][x]:
                bingo = False
                break
        if bingo:
            return True
    
    return False

def calculate_score(n, board, check_board):
    send = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if not check_board[y][x]:
                send += board[y][x]
    return send * n

with open("day4input.txt") as f:
    drawn_numbers = [int(x) for x in f.readline().split(',')]
    boards = [x.strip() for x in f.readlines()]
for x in range(len(boards)):
    boards[x] = boards[x].split(' ')
    boards[x] = list(filter(None, boards[x]))
boards = list(filter(None, boards))
for x in range(len(boards)):
    boards[x] = [int(y) for y in boards[x]]
boards = [boards[x : x + board_size] for x in range(0, len(boards), board_size)]

last_number = 0
winner_index = 0
winner_found = False
check_boards = list()
for i in range(len(boards)):
    tmp = list()
    for j in range(board_size):
        tmp.append([False] * board_size)
    check_boards.append(tmp)

for i in drawn_numbers:
    for j in range(len(boards)):
        check_boards[j] = mark_board(i, boards[j], check_boards[j])
        if has_bingo(check_boards[j]):
            last_number = i
            winner_found = True
            winner_index = j
            break
    if winner_found:
        break

print("The first answer is: ", calculate_score(last_number, boards[winner_index], check_boards[winner_index]))    

last_number = 0
winner_index = 0
winners_found = 0
winners = [False] * len(boards)
check_boards = list()
for i in range(len(boards)):
    tmp = list()
    for j in range(board_size):
        tmp.append([False] * board_size)
    check_boards.append(tmp)

for i in drawn_numbers:
    for j in range(len(boards)):
        check_boards[j] = mark_board(i, boards[j], check_boards[j])
        if has_bingo(check_boards[j]) and not winners[j]:
            last_number = i
            winners[j] = True
            winners_found += 1
            winner_index = j
    if winners_found >= len(boards):
        break
print("The second answer is: ", calculate_score(last_number, boards[winner_index], check_boards[winner_index]))

print("Execution time: ", (time.perf_counter()-t)*1000, "ms")