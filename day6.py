# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 14:54:39 2021

@author: AntonLundgren
"""
import numpy as np
import time
t = time.perf_counter()

def simulate_lanternfish(start_population, number_of_days):
    aged_fish = np.zeros(7, dtype='int64')
    smol_fish = np.zeros(2, dtype='int64')
    for fish in start_population:
        aged_fish[fish] += 1
    for day in range(number_of_days):
        new_fishy = aged_fish[0]
        aged_fish = np.roll(aged_fish, -1)
        aged_fish[6] += smol_fish[0]
        smol_fish[0] = smol_fish[1]
        smol_fish[1] = new_fishy    
    return sum(aged_fish) + sum(smol_fish)


start_population = np.genfromtxt("day6input.txt", delimiter=',', dtype=int)
print("The first answer is:", simulate_lanternfish(start_population, 80))
print("The second answer is:", simulate_lanternfish(start_population, 256))

print("Execution time was:", int((time.perf_counter() - t) * 1000), "ms")