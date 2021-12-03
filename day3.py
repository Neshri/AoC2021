#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 11:50:06 2021

@author: neshri
"""
number_of_bits = 12

with open("day3input.txt") as f:
    numbers = [int(x.strip(), base=2) for x in f.readlines()]

gamma = epsilon = 0
bitcount = [0] * number_of_bits

for x in numbers:
    for y in range(number_of_bits-1, -1, -1):
        bitcount[y] += x % 2
        x = x // 2

for x in bitcount:
    gamma = gamma << 1
    if x > len(numbers) / 2:
        gamma += 1

epsilon = gamma ^ int('1'*number_of_bits, 2)
print("Gamma: ", format(gamma, '012b'))
print("Epsilon: ", format(epsilon, '012b'))
print("The first answer is: ", gamma * epsilon)

oxygen_rating = co2_rating = 0
#Oxygen calculation
arr = numbers.copy()
shift = number_of_bits-1
while(len(arr) > 1):
    one_counter = 0
    for x in arr:
        n = x >> shift
        one_counter += n % 2
    if one_counter >= len(arr) / 2:
        one_counter = 1
    else:
        one_counter = 0
    tmp_arr = arr.copy()
    for x in tmp_arr:
        n = x >> shift
        if n % 2 != one_counter:
            arr.remove(x)
    shift -= 1
oxygen_rating = arr[0]
#CO2 calculation
arr = numbers.copy()
shift = number_of_bits-1
while(len(arr) > 1):
    one_counter = 0
    for x in arr:
        n = x >> shift
        one_counter += n % 2
    if one_counter >= len(arr) / 2:
        one_counter = 0
    else:
        one_counter = 1
    tmp_arr = arr.copy()
    for x in tmp_arr:
        n = x >> shift
        if n % 2 != one_counter:
            arr.remove(x)
    shift -= 1
co2_rating = arr[0]
print("Oxygen generator rating: ", format(oxygen_rating, '012b'))
print("CO2 scrubber rating: ", format(co2_rating, '012b'))
print("The second answer is: ", oxygen_rating * co2_rating)