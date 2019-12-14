import numpy as np
import intcode
from enum import IntEnum

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    total = 4

with open('day11-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = intcode.IntcodeComputer(instr_list)

wall = np.zeros((200,200), np.uint8)
_wall = np.zeros((200,200), np.bool)
curr_coord = [100,100]
curr_direction = Direction.UP

import sys
if len(sys.argv) == 1 or sys.argv[1] == '1':
    print('Part 1')
    pass
elif sys.argv[1] == '2':
    # Part 2
    print('Part 2')
    wall[tuple(curr_coord)] = 1
else:
    print(sys.argv)

while True:
    comp.append_input(wall[tuple(curr_coord)])
    comp.run()
    if comp.state == intcode.RunState.FINISHED:
        break

    color = comp.get_stdout()
    turn = comp.get_stdout()

    wall[tuple(curr_coord)] = color
    _wall[tuple(curr_coord)] = 1

    curr_direction = Direction((curr_direction + 1 if turn==1 else curr_direction - 1) % Direction.total)
    if curr_direction == Direction.UP:
        curr_coord[0] -= 1
    elif curr_direction == Direction.RIGHT:
        curr_coord[1] += 1
    elif curr_direction == Direction.DOWN:
        curr_coord[0] += 1
    elif curr_direction == Direction.LEFT:
        curr_coord[1] -= 1

print(_wall.sum())

import matplotlib.pyplot as plt
plt.imshow(wall)
plt.show()
