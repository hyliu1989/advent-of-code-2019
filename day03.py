import numpy as np

def parse_one(s):
    instr = s[0]
    val = int(s[1:])
    if   instr == 'U':
        ret = (0, val)
    elif instr == 'D':
        ret = (0, -val)
    elif instr == 'L':
        ret = (-val, 0)
    elif instr == 'R':
        ret = (val, 0)
    else:
        raise ValueError()

    return np.array(ret)

with open('day03-input.txt','r') as f:
    wire1 = f.readline()
    wire2 = f.readline()
instr_list1 = wire1.split(',')
instr_list2 = wire2.split(',')

def find_boundary(instr_list):
    pos = np.array([0,0])
    minimum = np.array([0,0])
    maximum = np.array([0,0])

    for instr in instr_list:
        pos += parse_one(instr)
        minimum = np.minimum(minimum, pos)
        maximum = np.maximum(maximum, pos)

    return minimum, maximum

min1, max1 = find_boundary(instr_list1)
min2, max2 = find_boundary(instr_list2)
minimum = np.minimum(min1,min2)
maximum = np.maximum(max1,max2)

shape = maximum - minimum + 1

import sys
if sys.argv[1] == '1':
    # part 1
    def draw_one_wire(instr_list):
        canvas = np.zeros(shape, np.uint8)

        # initialize the position
        pos = np.array([0,0]) - minimum

        for instr in instr_list:
            pos_new = pos + parse_one(instr)
            if pos_new[0] == pos[0]:
                canvas[pos[0], min(pos_new[1], pos[1]):1+max(pos_new[1], pos[1])] += 1
            else:
                assert pos_new[1] == pos[1]
                canvas[min(pos_new[0], pos[0]):1+max(pos_new[0], pos[0]), pos[1]] += 1
            pos = pos_new
        canvas = (canvas != 0).astype(np.uint8)
        return canvas
    wire1 = draw_one_wire(instr_list1)
    wire2 = draw_one_wire(instr_list2)
    i_s, j_s = np.where(wire1+wire2 == 2)
    x_s, y_s = i_s + minimum[0], j_s + minimum[1]
    dist = abs(x_s) + abs(y_s)
    print(sorted(dist))

elif sys.argv[1] == '2':
    # part 2
    def draw_one_wire(instr_list):
        """Draw the canvas with the steps to reach each grid point
        """
        canvas = -np.ones(shape, np.int64)
        step = 0

        # initialize the position
        pos = np.array([0,0]) - minimum
        canvas[pos[0], pos[1]] = step

        for instr in instr_list:
            pos_new = pos + parse_one(instr)
            if pos_new[0] == pos[0]:
                # canvas[pos[0], min(pos_new[1], pos[1]):1+max(pos_new[1], pos[1])] += 1
                beg = min(pos_new[1], pos[1])+1
                end = max(pos_new[1], pos[1])+1
                for j in range(beg,end):
                    step += 1
                    if canvas[pos[0], j] == -1:
                        canvas[pos[0], j] = step

            else:
                assert pos_new[1] == pos[1]
                # canvas[min(pos_new[0], pos[0]):1+max(pos_new[0], pos[0]), pos[1]] += 1
                beg = min(pos_new[0], pos[0])+1
                end = max(pos_new[0], pos[0])+1
                for i in range(beg,end):
                    step += 1
                    if canvas[i,pos[1]] == -1:
                        canvas[i,pos[1]] = step
            pos = pos_new
        return canvas
    wire1 = draw_one_wire(instr_list1)
    wire2 = draw_one_wire(instr_list2)
    i_s, j_s = np.where((wire1!=-1).astype(np.uint8)+(wire2!=-1).astype(np.uint8) == 2)
    step_canvas = wire1+wire2
    step_of_intersections = []
    for i,j in zip(i_s,j_s):
        if step_canvas[i,j] != 0:
            step_of_intersections.append(step_canvas[i,j])
    print(min(step_of_intersections))
