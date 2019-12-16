import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day15-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]


move_vec_mapping = {
    1: np.array([-1, 0]),  # north
    2: np.array([ 1, 0]),  # south
    3: np.array([ 0,-1]),  # west
    4: np.array([ 0, 1]),  # east
}
def get_move_vector(direction):
    return move_vec_mapping[direction]

vec_to_direction_map = {
    (-1, 0): 1,
    ( 1, 0): 2,
    ( 0,-1): 3,
    ( 0, 1): 4,
}
def get_direction(pos_diff):
    return vec_to_direction_map[tuple(pos_diff)]

opposite_move_mapping = {
    1:2,
    2:1,
    3:4,
    4:3,
}
def get_opposite_move(direction):
    return opposite_move_mapping[direction]



map_type = -np.ones((500,500), np.int)
map_step = -np.ones((500,500), np.int)


