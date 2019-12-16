import numpy as np
map = np.load('map.npy')

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

def explore_3(pos, prev_move):
    to_explore = [1,2,3,4]
    if prev_move == 1:
        to_explore.remove(2)
    elif prev_move == 2:
        to_explore.remove(1)
    elif prev_move == 3:
        to_explore.remove(4)
    elif prev_move == 4:
        to_explore.remove(3)
    to_explore = np.array(to_explore)

    valid = np.zeros(3, np.int8)
    new_pos_s = np.zeros(3, object)
    for i, direction in enumerate(to_explore):
        new_pos = get_new_pos(pos, direction)
        valid[i] = map[tuple(new_pos)]
        new_pos_s[i] = new_pos

    return to_explore, new_pos_s, valid


def start_new_path(curr_pos, to_move, curr_steps):
    curr_pos = get_new_pos(curr_pos, to_move)
    prev_move = to_move
    curr_steps = curr_steps + 1

    while True:
        to_explore, new_pos_s, valid = explore_3(curr_pos, prev_move)
        if np.any(valid == 2):
            curr_steps += 1
            return curr_steps
        logic = valid == 1
        
        if logic.sum() == 0:
            return -1
        if logic.sum() == 1:
            curr_pos = new_pos_s[logic][0]
            prev_move = to_explore[logic][0]
            curr_steps += 1
        else:
            ret_step = -1
            for i in range(3):
                if logic[i] == False:
                    continue
                ret_step = start_new_path(curr_pos=curr_pos, to_move=to_explore[i], curr_steps=curr_steps)
                if ret_step != -1:
                    return ret_step
            return -1

steps = start_new_path(np.array([250,250], np.uint32), 4, 0)
print(steps)
