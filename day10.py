CHUNK_STARTS = ('(', '[', '{', '<')
CHUNK_ENDS = {'(': ')', '[': ']', '{': '}', '<': '>'}
CORRUPT_SCORE_TABLE = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETE_SCORE_TABLE = {')': 1, ']': 2, '}': 3, '>': 4}
with open("day10input.txt") as f:
    lines = [x.strip() for x in f.readlines()]

score_sum = 0
clean_lines = [x for x in lines]
for line in lines:
    stack = list()
    for i in line:
        if i in CHUNK_STARTS:
            stack.append(i)
        else:
            if i == CHUNK_ENDS[stack[len(stack) - 1]]:
                stack.pop()
            else:
                score_sum += CORRUPT_SCORE_TABLE[i]
                clean_lines.remove(line)
                break

print("The first answer is:", score_sum)

line_scores = list()
for line in clean_lines:
    stack = list()
    for i in line:
        if i in CHUNK_STARTS:
            stack.append(i)
        else:
            if i == CHUNK_ENDS[stack[len(stack) - 1]]:
                stack.pop()
    line_score = 0
    while len(stack) > 0:
        token = stack.pop()
        line_score *= 5
        line_score += COMPLETE_SCORE_TABLE[CHUNK_ENDS[token]]
    line_scores.append(line_score)

line_scores = sorted(line_scores)
answer = line_scores[int((len(line_scores) / 2))]
print("The second answer is:", answer)