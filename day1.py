#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 15:30:14 2021

@author: neshri
"""

with open("day1input.txt") as f:
    depths = [int(x) for x in f.readlines()]
    
previous = depths[0]
count = 0
for x in depths:
    if x > previous:
        count += 1
    previous = x
print("First answer is: ", count)

count = 0
for x in range(4, len(depths)+1):
    if sum(depths[x-4:x-1]) < sum(depths[x-3:x]):
        count += 1
print("Second answer is: ", count)