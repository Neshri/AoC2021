from collections import deque
import time
t = time.perf_counter()

def modulo_without_zero(n, m):
    n = (n-1) % (m-1)
    n += 1
    return n


def quantum_triple_roll_sum():
    outcomes = dict()
    for i in range(3, 10):
        outcomes[i] = 0
    for x in range(1, 4):
        for y in range(1, 4):
            for z in range(1, 4):
                outcomes[x+y+z] += 1
    return outcomes


with open("day21input.txt") as f:
    start = [int(f.readline().split(':')[1].strip()), int(f.readline().split(':')[1].strip())]

# Part 1
die = 0
player_scores = [0, 0]
player_pos = [start[0], start[1]]
cast_counter = 0
turn = 0
while player_scores[0] < 1000 and player_scores[1] < 1000:
    dice_sum = 0
    for i in range(3):
        die = modulo_without_zero(die+1, 101)
        dice_sum += die
    cast_counter += 3
    player_pos[turn] = modulo_without_zero(player_pos[turn] + dice_sum, 11)
    player_scores[turn] += player_pos[turn]
    turn = (turn + 1) % 2
print("The first answer is:", min(player_scores) * cast_counter)

# Part 2
rolls = quantum_triple_roll_sum()
state_lookup = dict()
game_state = ({"position": start[0], "dimensions": 1, "score": 0, "id": 0}, {"position": start[1], "dimensions": 1, "score": 0, "id": 1})
state_lookup[(0, start[0], 0, start[1], 0)] = 1
turn_stepper = deque()
turn_stepper.appendleft(game_state)
wins = [0, 0]
while len(turn_stepper) > 0:
    player1, player2 = turn_stepper.pop()
    state = (player1["id"], player1["position"], player1["score"], player2["position"], player2["score"])
    player1["dimensions"] = state_lookup[state]
    del state_lookup[state]
    for roll in rolls.keys():
        new_pos = modulo_without_zero(roll+player1["position"], 11)
        new_dims = player1["dimensions"] * rolls[roll]
        new_score = player1["score"] + new_pos
        if new_score >= 21:
            wins[player1["id"]] += new_dims
        else:
            state = (player2["id"], player2["position"], player2["score"], new_pos, new_score)
            if state not in state_lookup.keys():
                state_lookup[state] = new_dims
                turn_stepper.appendleft((player2, {"position": new_pos, "dimensions": new_dims, "score": new_score, "id": player1["id"]}))
            else:
                state_lookup[state] += new_dims
    
print("The second answer is:", max(wins))
print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")