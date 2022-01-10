from collections import deque
import time
import math

t = time.perf_counter()

class snailfish_number:

    
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def add(self, s_number):

        new_number = snailfish_number(self.deep_copy(), s_number.deep_copy())
        new_number.left.set_parent(new_number)
        new_number.right.set_parent(new_number)
        new_number.reduce()
        return new_number

    def deep_copy(self):
        if type(self.left) == int:
            left = self.left
        else:
            left = self.left.deep_copy()
        if type(self.right) == int:
            right = self.right
        else:
            right = self.right.deep_copy()
        new_number = snailfish_number(left, right)
        if type(new_number.left) == snailfish_number:
            new_number.left.set_parent(new_number)
        if type(new_number.right) == snailfish_number:
            new_number.right.set_parent(new_number)
        
        return new_number

    # 3 * left + 2 * right
    def magnitude(self):
        if type(self.left) == snailfish_number:
            left = self.left.magnitude()
        else:
            left = self.left
        if type(self.right) == snailfish_number:
            right = self.right.magnitude()
        else:
            right = self.right
        return 3 * left + 2 * right

    def __str__(self) -> str:
        return '[' + str(self.left) +','+ str(self.right) + ']'

    def reduce(self):
        while True:
            if self.explode():
                pass
            elif self.split():
                pass
            else:
                break

    
    

    def explode(self):
        queue = deque()
        depth = 0
        queue.append((self, depth))
        while len(queue) > 0:
            current, depth = queue.pop()
            if depth >= 4 and type(current.left) == int and type(current.right) == int:
                add_to_adjacent(current, current.left, "left")
                add_to_adjacent(current, current.right, "right")

                if current.parent.left == current:
                    current.parent.left = 0
                else:
                    current.parent.right = 0
                
                return True

            if type(current.right) == snailfish_number:
                queue.append((current.right, depth+1))
            if type(current.left) == snailfish_number:
                queue.append((current.left, depth+1))
        return False
        

    def split(self):
        queue = deque()
        queue.append((self, self.parent))
        while len(queue) > 0:
            current, current_parent = queue.pop()
            if type(current) == int and current > 9:
                if current == current_parent.left:
                    current_parent.left = snailfish_number(current // 2, int(math.ceil(current / 2)))
                    current_parent.left.set_parent(current_parent)
                else:
                    current_parent.right = snailfish_number(current // 2, int(math.ceil(current / 2)))
                    current_parent.right.set_parent(current_parent)
                return True
            if type(current) == snailfish_number:
                queue.append((current.right, current))
                queue.append((current.left, current))
        return False

def add_to_adjacent(sf_number, regular_number, direction):
    if sf_number.parent == None:
        return
    parent = sf_number.parent
    child = sf_number
    # Go up
    while parent.left is child and direction == "left" or parent.right is child and direction == "right":
        if parent.parent == None:
            return
        child = parent
        parent = parent.parent
    if type(parent.left) == int and direction == "left":
        parent.left += regular_number
        return
    elif type(parent.right) == int and direction == "right":
        parent.right += regular_number
        return
    # Go down
    if direction == "left":    
        current_node = parent.left
    elif direction == "right":
        current_node = parent.right
    if direction == "left":
        while type(current_node.right) != int:
            current_node = current_node.right
        current_node.right += regular_number
    elif direction == "right":
        while type(current_node.left) != int:
            current_node = current_node.left
        current_node.left += regular_number
    

 
def midpoint(string):
    depth = 0
    min_depth = len(string)
    mid_index = len(string) // 2
    for i in range(len(string)):
        if string[i] == '[':
            depth += 1
        elif string[i] == ']':
            depth -= 1
        elif string[i] == ',':
            if depth < min_depth:
                min_depth = depth
                mid_index = i

    return mid_index

def create_from_string(string) -> snailfish_number:
        def create_number(string):
            mid = midpoint(string)
            if string[mid-1] != ']':
                left = int(string[mid-1])
            else:
                left = create_number(string[1:mid])
            if string[mid+1] != '[':
                right = int(string[mid+1])
            else:
                right = create_number(string[mid+1:-1])
            n = snailfish_number(left, right)
            return n
            
        number = create_number(string)
        
        return number

with open("day18input.txt") as f:
    snailfish_numbers = [x.strip() for x in f.readlines()]
for i in range(len(snailfish_numbers)):
    snailfish_numbers[i] = create_from_string(snailfish_numbers[i])

# Give parents to children
for x in snailfish_numbers:
    queue = deque()
    queue.append(x)
    while len(queue) > 0:
        parent = queue.pop()
        if type(parent.left) == snailfish_number:
            parent.left.set_parent(parent)
            queue.append(parent.left)
        if type(parent.right) == snailfish_number:
            parent.right.set_parent(parent)
            queue.append(parent.right)

snailfish_sum = snailfish_numbers[0].deep_copy()
for x in snailfish_numbers[1:]:
    snailfish_sum = snailfish_sum.add(x)


print("The first answer is:", snailfish_sum.magnitude())

largest_sum = 0
for i in range(len(snailfish_numbers)):
    for j in range(i+1, len(snailfish_numbers)):
        tmp = snailfish_numbers[i].add(snailfish_numbers[j])
        tmp = tmp.magnitude()
        if tmp > largest_sum:
            largest_sum = tmp
        tmp = snailfish_numbers[j].add(snailfish_numbers[i])
        tmp = tmp.magnitude()
        if tmp > largest_sum:
            largest_sum = tmp

print("The second answer is:", largest_sum)

print("The execution time was:", int((time.perf_counter() - t) * 1000), "ms")