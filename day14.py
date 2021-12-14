from collections import deque

RULES = dict()

#Part 1 Solution
def real_step(polymer):
    send = deque()
    last = polymer.popleft()
    send.append(last)
    for x in polymer:
        rule = RULES.get(last + x)
        if rule == None:
            send.append(x)
        else:
            send.append(rule)
            send.append(x)
        last = x
    return send

#Part 2 Solution
def false_step(pair_hist, letter_hist):
    new_hist = dict()
    for x in RULES.keys():
        new_hist[x] = 0
    for x in pair_hist.keys():
        new_hist[x[0] + RULES[x]] += pair_hist[x]
        new_hist[RULES[x] + x[1]] += pair_hist[x]
        letter_hist[RULES[x]] += pair_hist[x]
    return new_hist

#Read and polish the input
with open("day14input.txt") as f:
    polymer = list(f.readline().strip())
    rules_input = [x.strip() for x in f.readlines()]
    rules_input.remove('')
for rule in rules_input:
    tmp = rule.split("->")
    tmp = [x.strip() for x in tmp]
    RULES[tmp[0]] = tmp[1]
original_polymer = polymer
polymer = deque(polymer)

# Part 1
for n in range(10):
    polymer = real_step(polymer)
letter_hist = dict()
for x in polymer:
    if x not in letter_hist.keys():
        letter_hist[x] = 1
    else:
        letter_hist[x] += 1

print("The first answer is:", max(letter_hist.values()) - min(letter_hist.values()))

# Part 2
letter_hist = dict()
for l in range(ord('A'), ord('Z') + 1):
    letter_hist[chr(l)] = 0
pair_hist = dict()
for x in RULES.keys():
    pair_hist[x] = 0
polymer = original_polymer
last = polymer[0]
letter_hist[last] += 1
for x in polymer[1:]:
    pair_hist["".join([last, x])] += 1
    letter_hist[x] += 1
    last = x
#Step 40 times
for n in range(40):
    pair_hist = false_step(pair_hist, letter_hist)

#Find min and max
ma = max(letter_hist.values())
mi = ma
for x in letter_hist.values():
    if x < mi and x > 0:
        mi = x
print("The second answer is:", ma - mi)


