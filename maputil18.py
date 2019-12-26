import numpy as np
import contexttimer
import sys
import numba
# part_id = int(sys.argv[1])
part_id = 0

# from intcode import IntcodeComputer, RunState
from direction import Direction, get_opposite, get_new_position, explore


wall = -999
def parse(c):
    if c == '#':
        return wall
    if c == '.':
        return 0
    if c == '@':
        return 999
    if ord('a') <= ord(c) <= ord('z'):
        return ord(c) - ord('a') + 1
    if ord('A') <= ord(c) <= ord('Z'):
        return -(ord(c) - ord('A') + 1)

with open('day18-input.txt', 'r') as f:
    init_map = []
    while True:
        line_str = f.readline()
        if line_str == '':
            break
        line_str = line_str.rstrip('\n')
        line = [parse(c) for c in line_str]
        init_map.append(line)
init_map = np.array(init_map)


"""
Singly-connected segment

A Segment does not have branches or forks. A Segment's head is inside
the singly-connected segment while its inclusive tail can be the joint of
a fork. Its ordered items are ordered according to the step to the maze
center (fewest to most).

"""
map_segment = np.zeros(init_map.shape, np.int64)
map_steps_from_parent = np.zeros(init_map.shape, np.int64)

n_segments_max = 512
n_items_max = 16
n_children_max = 3
db = - np.ones((n_segments_max, 5+n_children_max+n_items_max), np.int64)

ind_id = 0
ind_parent = 1
ind_iter_children = 2
ind_iter_items = 5  # items are in order
ind_length = 21
ind_quadrant = 22
ind_steps = 23  # steps to before quadrant head
db[:, ind_iter_items:ind_iter_items+n_items_max] = 0

db_ordered_item = db[:, ind_iter_items:   ind_iter_items   +n_items_max   ]
db_children     = db[:, ind_iter_children:ind_iter_children+n_children_max]


serial_to_assign = 0
def _make_segment(parent, step_from_parent_map_local:np.ndarray, children:list,
                  ordered_items:list, length:int, quadrant:int) -> int:
    global serial_to_assign, map_segment, map_steps_from_parent
    segment_id = serial_to_assign
    row = segment_id
    db[row, ind_id] = segment_id
    db[row, ind_parent] = parent
    for i,c in enumerate(children):
        db[row, ind_iter_children+i] = c
    for i,item in enumerate(ordered_items):
        db[row, ind_iter_items+i] = item
    db[row, ind_length] = length
    db[row, ind_quadrant] = quadrant
    if parent == -1:
        db[row, ind_steps] = 0
    else:
        db[row, ind_steps] = db[parent, ind_steps] + db[parent, ind_length]

    serial_to_assign += 1
    logic = (step_from_parent_map_local!=0)
    map_segment[logic] = segment_id
    assert np.all(map_steps_from_parent[logic] == 0)
    map_steps_from_parent[logic] = step_from_parent_map_local[logic]

    return segment_id

def _append_child(segment_id, child_id):
    # find the unassigned spot
    for i in range(n_children_max):
        if db[segment_id, ind_iter_children+i] == -1:
            break
    db[segment_id, ind_iter_children+i] = child_id

def _remove_child(segment_id, child_id):
    # find the child
    for child_ind in range(n_children_max):
        if db[segment_id, ind_iter_children+child_ind] == child_id:
            break

    for i in range(child_ind, n_children_max):
        if i == n_children_max-1:
            db[segment_id, ind_iter_children+i] = -1
        else:
            db[segment_id, ind_iter_children+i] = db[segment_id, ind_iter_children+i+1]

def _is_position_valid(pos):
    return init_map[tuple(pos)] != wall

## Build segment map and locate items

item_positions = {}

def _make_segment_recursive(parent, pos, prev_move, quadrant)-> int:
    # Segment init required variables
    step_from_parent_map_local = np.zeros_like(init_map, dtype=np.uint8)
    collected_items = []
    nth_tile = 0

    while True:
        nth_tile += 1
        ij = tuple(pos)
        step_from_parent_map_local[ij] = nth_tile
        item = init_map[ij]
        if item != 0:
            item_positions[item] = ij
            collected_items.append(item)
        trace_heads = explore(pos, prev_move, _is_position_valid)
        num = len(trace_heads)
        if num == 0:
            # finalize the Segment
            ret = _make_segment(parent, step_from_parent_map_local, [], collected_items, nth_tile, quadrant)
            return ret
        elif num == 1:
            # continue
            pos, prev_move = trace_heads[0]
        elif num >= 2:
            # finalize the Segment and start new searches
            ret = _make_segment(parent, step_from_parent_map_local, [], collected_items, nth_tile, quadrant)
            for i in range(num):
                pos, prev_move = trace_heads[i]
                _append_child(ret, _make_segment_recursive(ret, pos, prev_move, quadrant))
            return ret


quadrants = [None] * 4
quadrants[0] = [_make_segment_recursive(-1, np.array([39,42]), Direction.EAST,  0),
                _make_segment_recursive(-1, np.array([38,41]), Direction.NORTH, 0),]

quadrants[1] = [_make_segment_recursive(-1, np.array([38,39]), Direction.NORTH, 1),
                _make_segment_recursive(-1, np.array([39,38]), Direction.WEST,  1),]

quadrants[2] = [_make_segment_recursive(-1, np.array([41,38]), Direction.WEST,  2),
                _make_segment_recursive(-1, np.array([42,39]), Direction.SOUTH, 2),]

quadrants[3] = [_make_segment_recursive(-1, np.array([42,41]), Direction.SOUTH, 3),]


def _trim(segment_id):
    """trim out the branches that contains no keys"""
    to_remove = []
    branch_has_key = False
    for i in range(n_items_max):
        item = db[segment_id,ind_iter_items+i]
        if item == 0:
            break
        if 1 <= item <= 26:
            branch_has_key = True
            break

    for i in range(n_children_max):
        child = db[segment_id, ind_iter_children+i]
        if child == -1:
            break
        child_has_key = _trim(child)
        if not child_has_key:
            to_remove.append(child)
        else:
            branch_has_key = True

    for child in to_remove:
        _remove_child(segment_id, child)

    return branch_has_key


for quad in quadrants:
    for s in quad:
        _trim(s)
del quad, s

def visualize_trimmed():
    trimmed_map = np.zeros_like(init_map)
    def paint(segment_id):
        trimmed_map[map_segment==segment_id] = 2
        for i in range(n_children_max):
            c = db[segment_id, ind_iter_children+i]
            if c != -1:
                paint(c)
    for quad in quadrants:
        for s in quad:
            paint(s)

    for k in item_positions:
        if k > 0:
            i,j = item_positions[k]
            trimmed_map[i,j] = 1
    return trimmed_map

@numba.jit(nopython=True, nogil=True)
def _build_parent_list(segment_id, db=db, ind_parent=ind_parent):
    parent_list = -np.ones((128,), np.int64)
    idx = 0
    parent_list[idx] = segment_id

    while True:
        p = db[parent_list[idx],ind_parent]
        idx += 1
        parent_list[idx] = p
        if p == -1:
            break
    return parent_list, idx

@numba.jit(nopython=True, nogil=True)
def _find_common_parent(seg1:int, seg2:int, db=db, ind_quadrant=ind_quadrant, ind_parent=ind_parent):
    # no common parent because they are in different quadrant
    if db[seg1, ind_quadrant] != db[seg2, ind_quadrant]:
        return None

    # build up a parent lists
        
    parent_list1, idx_max_1 = _build_parent_list(seg1, db, ind_parent)
    parent_list2, idx_max_2 = _build_parent_list(seg2, db, ind_parent)

    # check the other trace
    for common_ind in range(128):
        if parent_list1[idx_max_1-common_ind] != parent_list2[idx_max_2-common_ind]:
            break
    common_ind -= 1

    return parent_list1[idx_max_1-common_ind]
    # if p == -1, that means they are in different main branches of the same quadrant


@numba.jit('i8(i8,i8,i8[:,:],i8,i8)', nopython=True, nogil=True)
def count_steps_until_entering_the_ancestor(segment_id, ancestor_seg=-1, db=db,
                                            ind_steps=ind_steps, ind_length=ind_length):
    steps = db[segment_id, ind_steps]
    if ancestor_seg == -1:
        pass
    else:
        to_subtract = db[ancestor_seg, ind_steps] + db[ancestor_seg, ind_length]
        steps -= to_subtract
    return steps


@numba.jit('i8(i8,i8,i8,i8,i8[:,:], i8[:,:], i8[:,:], i8,i8,i8)', nopython=True, nogil=True)
def move(i_curr, j_curr, i_dest, j_dest, map_segment=map_segment, map_steps_from_parent=map_steps_from_parent,
         db=db, ind_steps=ind_steps, ind_quadrant=ind_quadrant, ind_length=ind_length):
    """Return the number of steps of this move

    current:  (i,j)-index of current position
    destination:  (i,j)-index of the destination
    """
    # count the step to move to where the key is
    dest_seg = map_segment[i_dest, j_dest]

    steps = 0

    if i_curr == 40 and j_curr == 40:
        steps += map_steps_from_parent[i_dest, j_dest]
        steps += db[dest_seg,ind_steps]
        steps += 2
    else:
        head_seg = map_segment[i_curr, j_curr]
        if db[head_seg,ind_quadrant] != db[dest_seg,ind_quadrant]:
            # head and the key are in different quadrants
            steps += map_steps_from_parent[i_curr, j_curr]-1
            steps += db[head_seg, ind_steps]
            if (db[head_seg,ind_quadrant], db[dest_seg,ind_quadrant]) in [(0,2), (2,0), (1,3), (3,1)]:
                steps += 5
            else:
                steps += 3
            steps += db[dest_seg, ind_steps]
            steps += map_steps_from_parent[i_dest, j_dest]
        else:
            p1 = _find_common_parent(head_seg, dest_seg)
            # head and the key are in the same quadrant
            if p1 == dest_seg:
                steps += map_steps_from_parent[i_curr, j_curr] - 1
                steps += count_steps_until_entering_the_ancestor(head_seg, ancestor_seg=dest_seg, db=db, ind_steps=ind_steps, ind_length=ind_length)
                steps += db[dest_seg, ind_length] - map_steps_from_parent[i_dest, j_dest] + 1
            elif p1 == head_seg:
                steps += db[head_seg, ind_length] - map_steps_from_parent[i_curr, j_curr]
                steps += count_steps_until_entering_the_ancestor(dest_seg, ancestor_seg=head_seg, db=db, ind_steps=ind_steps, ind_length=ind_length)
                steps += map_steps_from_parent[i_dest, j_dest]
            else:
                # p1 is some segment in between or the head of the quadrant
                steps += map_steps_from_parent[i_curr, j_curr] - 1
                steps += count_steps_until_entering_the_ancestor(head_seg, ancestor_seg=p1, db=db, ind_steps=ind_steps, ind_length=ind_length)
                steps += 1
                steps += count_steps_until_entering_the_ancestor(dest_seg, ancestor_seg=p1, db=db, ind_steps=ind_steps, ind_length=ind_length)
                steps += map_steps_from_parent[i_dest, j_dest]

    return steps
