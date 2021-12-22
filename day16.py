
class packet:

    def __init__(self, version, type_id):
        self.value = 0
        self.version = version
        self.type_id = type_id
        self.sub_packets = list()

    def add_sub_packet(self, new_packet):
        self.sub_packets.append(new_packet)

    def __str__(self) -> str:
        return "".join((str(self.version), " : ", str(self.type_id), " : ", str(self.value)))

def type_4(bits, i):
    n = list()
    while True:
        last_group = True if bits[i] == '0' else False
        n.append(bits[i + 1: i + 5])
        i += 5
        if last_group:
            break
    n = int("".join(n), base=2)
    return (i, n)
    
def read_binary(bits, i, parent_packet):
    version, type_id = int(bits[i : i + 3], base=2), int(bits[i + 3: i + 6], base=2)
    new_packet = packet(version, type_id)
    parent_packet.add_sub_packet(new_packet)
    i += 6
    version_sum = version
    if type_id == 4:
        i, n = type_4(bits, i)
        new_packet.value = n
    else:
        if bits[i] == '0':
            i += 1
            end = int(bits[i : i + 15], base=2)
            i += 15
            end += i
            while i < end:
                tmp = read_binary(bits, i, new_packet)
                version_sum += tmp[0]
                i = tmp[1]
        elif bits[i] == '1':
            i += 1
            length = int(bits[i : i + 11], base=2)
            i += 11
            for x in range(length):
                tmp = read_binary(bits, i, new_packet)
                version_sum += tmp[0]
                i = tmp[1]
        #Operations
        if type_id == 0:
            value = 0
            for x in new_packet.sub_packets:
                value += x.value
            new_packet.value = value
        elif type_id == 1:
            value = 1
            for x in new_packet.sub_packets:
                value *= x.value
            new_packet.value = value
        elif type_id == 2:
            value = min([x.value for x in new_packet.sub_packets])
            new_packet.value = value
        elif type_id == 3:
            value = max([x.value for x in new_packet.sub_packets])
            new_packet.value = value
        elif type_id == 5:
            value = 1 if new_packet.sub_packets[0].value > new_packet.sub_packets[1].value else 0
            new_packet.value = value
        elif type_id == 6:
            value = 1 if new_packet.sub_packets[0].value < new_packet.sub_packets[1].value else 0
            new_packet.value = value
        elif type_id == 7:
            value = 1 if new_packet.sub_packets[0].value == new_packet.sub_packets[1].value else 0
            new_packet.value = value
    return (version_sum, i)

with open("day16input.txt") as f:
    line = f.readline().strip()

line = bin(int(line, base=16))[2:].zfill(len(line) * 4)
root = packet(0, 0)
version_sum = read_binary(line, 0, root)[0]
print("The first answer is:", version_sum)
print("The second answer is:", root.sub_packets[0].value)
