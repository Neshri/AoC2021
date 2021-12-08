# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:10:49 2021

@author: AntonLundgren
"""
DIGITS = {0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 4: "bcdf", 5: "abdf", 6: "abdefg", 7: "acf", 8: "abcdefg", 9: "abcdfg"}
LENGTH_DICT = {2:1, 4:4, 3:7, 7:8}
with open("day8input.txt") as f:
    lines = [x.strip().split(' ') for x in f.readlines()]
[x.remove('|') for x in lines]
for x in range(len(lines)):
    for y in range(len(lines[x])):
        lines[x][y] = "".join(sorted(lines[x][y]))

count = 0
for x in lines:
    for y in range(10, 14):
        if len(x[y]) in (2, 4, 3, 7):
            count += 1

print("The first answer is:", count)

count = 0
for x in lines:
    string_to_number = dict()
    number_to_string = dict()
    tmp = [[], []]
    for y in range(10):
        if len(x[y]) in (2, 4, 3, 7):
            # Decode 1 4 7 8
            string_to_number.update({x[y]: LENGTH_DICT[len(x[y])]})
            number_to_string.update({LENGTH_DICT[len(x[y])]: x[y]})
        elif len(x[y]) == 6:
            # save 0 6 9
            tmp[0].append(x[y])
        else:
            # save 2 3 5
            tmp[1].append(x[y])
    
    # Decode 6 9 0
    for y in tmp[0]:
        if not set(number_to_string[1]).issubset(y):
            string_to_number.update({y: 6})
            number_to_string.update({6: y})
        elif set(number_to_string[4]).issubset(y):
            string_to_number.update({y: 9})
            number_to_string.update({9: y})
        else:
            string_to_number.update({y: 0})
            number_to_string.update({0: y})
    
    # Decode 3 5 2
    for y in tmp[1]:
        if set(number_to_string[1]).issubset(y):
            string_to_number.update({y: 3})
            number_to_string.update({3: y})
        elif set(y).issubset(number_to_string[6]):
            string_to_number.update({y: 5})
            number_to_string.update({5: y})
        else:
            string_to_number.update({y: 2})
            number_to_string.update({2: y})
    output = []    
    for y in range(10, 14):
        output.append(string_to_number[x[y]])
    count += int("".join(map(str, output)))

print("The second answer is:", count)