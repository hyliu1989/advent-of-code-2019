import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day15-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

remote_control = IntcodeComputer(instr_list)

map = -np.ones((100,100), np.int8)
pos = np.array([ 50, 50], dtype=np.int32)
map[tuple(pos)] = 3

n_steps = 0
fh = figure()
ah = fh.add_subplot(111)
ah.imshow(map)
ih = ah.images[0]
fh.show()

def get_new_pos(pos, direction):
    if direction == 1:  # north
        new_pos = pos - [1,0]
    elif direction == 2:  # south
        new_pos = pos + [1,0]
    elif direction == 3:  # west
        new_pos = pos - [0,1]
    elif direction == 4:  # east
        new_pos = pos + [0,1]
    return new_pos


while True:
    direction = np.random.randint(4) + 1
    if direction == 1:  # north
        new_pos = pos - [1,0]
    elif direction == 2:  # south
        new_pos = pos + [1,0]
    elif direction == 3:  # west
        new_pos = pos - [0,1]
    elif direction == 4:  # east
        new_pos = pos + [0,1]
    remote_control.append_input(direction)
    remote_control.run()
    status = remote_control.get_stdout()

    if status == 0:
        map[tuple(new_pos)] = 0
    elif status == 1:
        map[tuple(new_pos)] = 1
        pos = new_pos
    elif status == 2:
        map[tuple(new_pos)] = 2
        pos = new_pos
        break
    if n_steps % 10000 == 0:
        print(n_steps)
        ih.set_data(map)
        fh.canvas.draw()
        pause(0.05)
    n_steps += 1
np.save('map.npy', map)

ih.set_data(map)
fh.canvas.draw()

