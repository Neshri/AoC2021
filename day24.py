import copy
from random import random
import time
t = time.perf_counter()


def recursive_run(instructions, instr_index, memory, inputs, inp_index, fail_set, divs_left, largest_nbr):
    if (inp_index, memory['z']) in fail_set:
        return -1

    # Test if it's possible to get back to z==0
    tmp = memory['z'] // (26**divs_left)
    if tmp > 0:
        fail_set.add((inp_index, memory['z']))
        return -1

    #Occasionally show progress at random intervals
    if random() > 0.999995:
        print(''.join([str(x) for x in inputs]), memory['z'], len(fail_set), inp_index)
        
    while instr_index < len(instructions):
        instr = instructions[instr_index]
        if instr[0] == 'div' and instr[1] == 'z' and instr[2] == 26:
            divs_left -= 1
        b = instr[2]
        if b in memory.keys():
            b = memory[b]
        match instr[0]:
            case "inp":                
                for i in range(9):
                    if largest_nbr:
                        inputs[inp_index] = 9 - i
                    else:
                        inputs[inp_index] = 1 + i
                    memory[instr[1]] = inputs[inp_index]
                    tmp = recursive_run(instructions, instr_index + 1, copy.deepcopy(memory), inputs, inp_index + 1, fail_set, divs_left, largest_nbr)
                    if tmp == 0:
                        return 0
                fail_set.add((inp_index+1, memory['z']))
                return -1
   
            case "add":
                memory[instr[1]] += b
            case "mul":
                memory[instr[1]] *= b
            case "div":
                memory[instr[1]] = memory[instr[1]] // b
            case "mod":
                memory[instr[1]] = memory[instr[1]] % b
            case "eql":
                memory[instr[1]] = 1 if memory[instr[1]] == b else 0
        instr_index += 1
    return memory['z']

def solution(instructions, memory, inputs, largest_nbr):
    fail_set = set()
    recursive_run(instructions, 0, copy.deepcopy(memory), inputs, 0, fail_set, 7, largest_nbr)
    return inputs

# Standard instruction runner
def run_instructions(instructions, memory, inputs):
    input_index = 0
    i = 0
    while i < len(instructions):
        instr = instructions[i]
        b = instr[2]
        if b in memory.keys():
            b = memory[b]
        match instr[0]:
            case "inp":
                memory[instr[1]] = inputs[input_index]
                input_index += 1
            case "add":
                memory[instr[1]] += b
            case "mul":
                memory[instr[1]] *= b
            case "div":
                memory[instr[1]] = memory[instr[1]] // b
            case "mod":
                memory[instr[1]] = memory[instr[1]] % b
            case "eql":
                memory[instr[1]] = 1 if memory[instr[1]] == b else 0
        i += 1
    return memory

def nbr_to_arr(n):
    send = [0] * 14
    for i in reversed(range(14)):
        send[i] = n % 10
        n = n // 10

    return send


with open("day24input.txt") as f:
    instructions = [x.strip() for x in f.readlines()]
for i in range(0, len(instructions)):
    tmp = instructions[i].split(' ')
    instr = tmp[0]
    a = tmp[1]
    if instr == "inp":
        instructions[i] = [instr, a, 0]
    else:
        b = tmp[2]
        try:
            n = int(b)
            b = n
        except ValueError:
            pass
        instructions[i] = [instr, a, b]

# Get largest
memory = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
model_number = [9] * 14
model_number = solution(instructions, memory, model_number, True)
print('The first answer is:', ''.join([str(x) for x in model_number]))

# Get smallest
memory = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
model_number = [1] * 14
model_number = solution(instructions, memory, model_number, False)
print('The second answer is:', ''.join([str(x) for x in model_number]))

print('The execution time was:', int((time.perf_counter() - t) * 1000), 'ms')
