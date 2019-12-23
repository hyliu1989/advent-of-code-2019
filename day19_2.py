import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day19-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]
    instr_list = np.array(instr_list)

def query_a_point(x,y):
    comp = IntcodeComputer(instr_list)
    comp.stdin = (x,y)
    comp.run()
    return comp.stdout

def find_transition(x_range, y):
    """return the point after transition"""
    x_range = x_range.copy()
    end_type = query_a_point(x_range[-1], y)
    if query_a_point(x_range[0], y) == end_type:
        raise RuntimeError('Range error')

    while x_range[-1] - x_range[0] != 1:
        x = (x_range[-1] + x_range[0]) // 2
        curr = query_a_point(x, y)
        if curr != end_type:
            x_range[0] = x
        else:
            x_range[-1] = x
    return x_range[-1]

# find the first line that fits
for ind in range(15,25): 
    y,x = np.array([48,26]) * ind
    
    if query_a_point(x-40,y) != 1:
        continue

    if query_a_point(x+40,y) != 1:
        continue

    break

start_x = find_transition([x-60, x-40], y)
end_x = find_transition([x+40, x+60], y)
range_len = 20

start_y = y


def get_x_range(y):
    return [int(y/start_y*start_x)-range_len, int(y/start_y*start_x)+range_len]

def test_y_contains_santa(y):
    try:
        x = find_transition(get_x_range(y), y)
    except:
        range_len *= 2
        x = find_transition(get_x_range(y), y)
    if query_a_point(x,y-100+1) == 1 and query_a_point(x+100-1,y-100+1) == 1:
        return True, x
    else:
        return False, x

def find_y(y_range):
    y_range = y_range.copy()

    while y_range[-1]-y_range[0] != 1:
        y = (y_range[-1]+y_range[0])//2
        it_contains, x = test_y_contains_santa(y)
        if it_contains:
            y_range[-1] = y
        else:
            y_range[0] = y

    return {'y':y_range[-1], 'x':x}


for ind in range(1,10):
    y = start_y*ind
    it_contains, x = test_y_contains_santa(y)
    if it_contains:
        print(x,y)
        break
    del y

res = find_y([start_y, y])
res['y'] -= (100-1)
print(res)
