# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:10:49 2021

@author: AntonLundgren
"""
DIGITS = {0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 4: "bcdf",
          5: "abdf", 6: "abdefg", 7: "acf", 8: "abcdefg", 9: "abcdfg"}
LENGTH_DICT = {2: 1, 4: 4, 3: 7, 7: 8}
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
    nonunique = [[], []]
    for y in range(10):
        if len(x[y]) in (2, 4, 3, 7):
            # Decode 1 4 7 8
            string_to_number.update({x[y]: LENGTH_DICT[len(x[y])]})
            number_to_string.update({LENGTH_DICT[len(x[y])]: x[y]})
        elif len(x[y]) == 6:
            # save 0 6 9
            nonunique[0].append(x[y])
        else:
            # save 2 3 5
            nonunique[1].append(x[y])

    # Decode 6 9 0
    for i in nonunique[0]:
        if not set(number_to_string[1]).issubset(i):
            string_to_number.update({i: 6})
            number_to_string.update({6: i})
        elif set(number_to_string[4]).issubset(i):
            string_to_number.update({i: 9})
            number_to_string.update({9: i})
        else:
            string_to_number.update({i: 0})
            number_to_string.update({0: i})

    # Decode 3 5 2
    for i in nonunique[1]:
        if set(number_to_string[1]).issubset(i):
            string_to_number.update({i: 3})
            number_to_string.update({3: i})
        elif set(i).issubset(number_to_string[6]):
            string_to_number.update({i: 5})
            number_to_string.update({5: i})
        else:
            string_to_number.update({i: 2})
            number_to_string.update({2: i})
    
    # Add output to counter
    output = ""
    for y in range(10, 14):
        output += str(string_to_number[x[y]])
    count += int(output)

print("The second answer is:", count)
