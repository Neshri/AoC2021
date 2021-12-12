import copy
import time
t = time.perf_counter()

CAVES = set()
LINKS = {}

def dfs(current_cave, visits, current_path):
    current_path.append(current_cave)
    visits[current_cave] += 1
    if current_cave == "end":
        paths.add(tuple(current_path))
        return
    for x in LINKS[current_cave]:
        if x.islower():
            if visits[x] == 0:
                dfs(x, copy.deepcopy(visits), copy.deepcopy(current_path))
        else:
            dfs(x, copy.deepcopy(visits), copy.deepcopy(current_path))
    return


def special_dfs(current_cave, visits, current_path, caved_small_twice):
    current_path.append(current_cave)
    visits[current_cave] += 1
    if current_cave == "end":
        paths.add(tuple(current_path))
        return
    for x in LINKS[current_cave]:
        if x.islower():
            if visits[x] == 0:
                special_dfs(x, copy.deepcopy(visits), copy.deepcopy(current_path), caved_small_twice)
            elif visits[x] == 1 and not caved_small_twice and x != "start":
                special_dfs(x, copy.deepcopy(visits), copy.deepcopy(current_path), True)
        else:
            special_dfs(x, copy.deepcopy(visits), copy.deepcopy(current_path), caved_small_twice)
    return


with open("day12input.txt") as f:
    lines = [x.strip() for x in f.readlines()]
for x in lines:
    tmp = x.split('-')
    CAVES.add(tmp[0])
    CAVES.add(tmp[1])
    l = list()
    LINKS[tmp[0]] = l
    l = list()
    LINKS[tmp[1]] = l
for x in lines:
    tmp = x.split('-')
    LINKS[tmp[0]].append(tmp[1])
    LINKS[tmp[1]].append(tmp[0])

paths = set()
visits = {}
for x in CAVES:
    visits[x] = 0
current_path = list()
dfs("start", visits, current_path)
print("The first answer is:", len(paths))

paths = set()
visits = {}
for x in CAVES:
    visits[x] = 0
current_path = list()
special_dfs("start", visits, current_path, False)
print("The second answer is:", len(paths))

print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")