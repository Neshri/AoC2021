#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 14:50:58 2021

@author: neshri
"""

with open("day2input.txt") as f:
    commands = [x.strip() for x in f.readlines()]

#First part
pos = [0, 0]
for x in commands:
    c = x.split(' ')
    c[1] = int(c[1])
    if c[0] == "up":
        pos[1] -= c[1]
    elif c[0] == "down":
        pos[1] += c[1]
    elif c[0] == "forward":
        pos[0] += c[1]

print("The first answer is: ", pos[0] * pos[1])

#Second part
pos = [0, 0, 0]
for x in commands:
    c = x.split(' ')
    c[1] = int(c[1])
    if c[0] == "up":
        pos[2] -= c[1]
    elif c[0] == "down":
        pos[2] += c[1]
    elif c[0] == "forward":
        pos[0] += c[1]
        pos[1] += c[1] * pos[2]

print("The second answer is: ", pos[0] * pos[1])