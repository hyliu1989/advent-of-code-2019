import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day17-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = IntcodeComputer(instr_list)
out = comp.run()

map = []
line = []
for c in out:
    if c == 46:
        line.append(0)
    elif c == 35:
        line.append(1)
    elif c == 10:
        map.append(line)
        line = []
    elif c == 94:   # ^
        line.append(11)
    elif c == 62:   # >
        line.append(12)
    elif c == 118:  # v
        line.append(13)
    elif c == 60:   # <
        line.append(14)
map = np.array(map[:-1])

alignment = 0
for i in range(1,map.shape[0]):
    for j in range(1,map.shape[1]):
        if map[i,j] == 0:
            continue
        if map[i-1,j] == 0:
            continue
        if map[i,j-1] == 0:
            continue
        if map[i+1,j] == 0:
            continue
        if map[i,j+1] == 0:
            continue
        print(i,j)
        alignment += i*j
print(alignment)
