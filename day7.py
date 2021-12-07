# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 19:54:19 2021

@author: AntonLundgren
"""

import numpy as np

def asum(n):
    return int((n * (1 + n)) / 2)

def fuel_cost_to(crabs, destination):
    cost = 0
    for crab in crabs:
        cost += asum(abs(crab - destination))
    return cost

crabs = np.genfromtxt("day7input.txt", delimiter=',', dtype='int64')
median = int(np.median(crabs))

answer = 0
for crab in crabs:
    answer += abs(crab - median)
print("The first answer is:", answer)

answer = 0
cheap_dest = int(round(np.mean(crabs)))
answer = fuel_cost_to(crabs, cheap_dest)
cheaper_direction = 0
tmp = fuel_cost_to(crabs, cheap_dest-1)
if tmp < answer:
    answer = tmp
    cheaper_direction = -1
else:
    cheaper_direction = 1
while cheaper_direction != 0:
    cheap_dest += cheaper_direction
    tmp = fuel_cost_to(crabs, cheap_dest)
    if tmp < answer:
        answer = tmp
    else:
        cheaper_direction = 0
print("The second answer is:", answer)