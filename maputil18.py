import numpy as np
import contexttimer
import sys
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
segment_map = np.zeros(init_map.shape, np.int64)
step_from_parent_map = np.zeros(init_map.shape, np.int64)

n_segments = 6400
n_item_max = 16
n_child_max = 3
segment_db = dict(
    serial =        -1 * np.ones((n_segments,),    np.int64), 
    parent =        -1 * np.ones((n_segments,),    np.int64),
    children =      -1 * np.ones((n_segments, n_child_max), np.int64),
    ordered_items = np.zeros((n_segments, n_item_max), np.int64),
    length =        -1 * np.ones((n_segments,),    np.int64),
    quadrant =      -1 * np.ones((n_segments,),    np.int64),
    n_steps_to_before_quadrant_head = -1 * np.ones((n_segments,), np.int64),
)
serial_to_assign = 0
def _make_segment(parent, step_from_parent_map_local:np.ndarray, children:list,
                  ordered_items:list, length:int, quadrant:int) -> int:
    global serial_to_assign, segment_map, step_from_parent_map
    ind = serial_to_assign
    segment_db['serial'][ind] = ind
    segment_db['parent'][ind] = parent
    for i,c in enumerate(children):
        segment_db['children'][ind,i] = c
    for i,item in enumerate(ordered_items):
        segment_db['ordered_items'][ind,i] = item
    segment_db['length'][ind] = length
    segment_db['quadrant'][ind] = quadrant
    if parent == -1:
        segment_db['n_steps_to_before_quadrant_head'][ind] = 0
    else:
        segment_db['n_steps_to_before_quadrant_head'][ind] = (
            segment_db['n_steps_to_before_quadrant_head'][parent] + segment_db['length'][parent]
        )

    serial_to_assign += 1
    logic = (step_from_parent_map_local!=0)
    segment_map[logic] = ind
    step_from_parent_map[logic] = step_from_parent_map_local[logic]

    return ind

def _append_child(serial, child_serial):
    # find the unassigned spot
    for i in range(n_child_max):
        if segment_db['children'][serial][i] == -1:
            break
    segment_db['children'][serial][i] = child_serial

def _remove_child(serial, child_serial):
    # find the child
    for child_ind in range(n_child_max):
        if segment_db['children'][serial][child_ind] == child_serial:
            break

    for i in range(child_ind, n_child_max):
        if i == n_child_max-1:
            segment_db['children'][serial][i] = -1
        else:
            segment_db['children'][serial][i] = segment_db['children'][serial][i+1]

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


def _trim(segment_serial):
    """trim out the branches that contains no keys"""
    to_remove = []
    branch_has_key = False
    for i in range(n_item_max):
        item = segment_db['ordered_items'][segment_serial,i]
        if item == 0:
            break
        if 1 <= item <= 26:
            branch_has_key = True
            break

    for i in range(n_child_max):
        child = segment_db['children'][segment_serial,i]
        if child == -1:
            break
        child_has_key = _trim(child)
        if not child_has_key:
            to_remove.append(child)
        else:
            branch_has_key = True

    for child in to_remove:
        _remove_child(segment_serial, child)

    return branch_has_key


for quad in quadrants:
    for s in quad:
        _trim(s)
del quad, s

def visualize_trimmed():
    trimmed_map = np.zeros_like(init_map)
    def paint(seg_serial):
        trimmed_map[segment_map==seg_serial] = 2
        for i in range(n_child_max):
            c = segment_db['children'][seg_serial,i]
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


def _find_common_parent(seg1:int, seg2:int):
    # no common parent because they are in different quadrant
    if segment_db['quadrant'][seg1] != segment_db['quadrant'][seg2]:
        return None

    # build up a parent list
    parent_list1 = [seg1]
    while True:
        p = segment_db['parent'][parent_list1[-1]]
        parent_list1.append(p)
        if p == -1:
            break
    # check the other trace
    p = seg2
    have_common_parent = True
    while True:
        if p in parent_list1 or p == -1:
            break
        p = segment_db['parent'][p]

    return p
    # if p == -1, that means they are in different main branches of the same quadrant


def count_steps_until_entering_the_ancestor(current_seg, *, ancestor_seg=None):
    step = 0
    p = segment_db['parent'][current_seg]
    while True:
        if p == ancestor_seg or p == -1:
            break
        step += segment_db['length'][p]
        p = segment_db['parent'][p]
    return step


def move(current, destination):
    """Return the number of steps of this move

    current:  (i,j)-index of current position
    destination:  (i,j)-index of the destination
    """
    # count the step to move to where the key is
    dest_seg = segment_map[destination]

    steps = 0

    if current == (40,40):
        steps += step_from_parent_map[destination]
        steps += segment_db['n_steps_to_before_quadrant_head'][dest_seg]
        assert (count_steps_until_entering_the_ancestor(dest_seg)
                == segment_db['n_steps_to_before_quadrant_head'][dest_seg])
        steps += 2
    else:
        head_seg = segment_map[current]
        if segment_db['quadrant'][head_seg] != segment_db['quadrant'][dest_seg]:
            # head and the key are in different quadrants
            steps += step_from_parent_map[current]-1
            steps += segment_db['n_steps_to_before_quadrant_head'][head_seg]
            if (segment_db['quadrant'][head_seg], segment_db['quadrant'][dest_seg]) in [(0,2), (2,0), (1,3), (3,1)]:
                steps += 5
            else:
                steps += 3
            steps += segment_db['n_steps_to_before_quadrant_head'][dest_seg]
            steps += step_from_parent_map[destination]
        else:
            p1, p2 = _find_common_parent(head_seg, dest_seg)
            assert p2 is None
            # head and the key are in the same quadrant
            if p1 is dest_seg:
                steps += step_from_parent_map[current] - 1
                steps += count_steps_until_entering_the_ancestor(
                    head_seg, ancestor_seg=dest_seg)
                steps += segment_db['length'][dest_seg] - step_from_parent_map[destination] + 1
            elif p1 is head_seg:
                steps += segment_db['length'][head_seg] - step_from_parent_map[current]
                steps += count_steps_until_entering_the_ancestor(
                    dest_seg, ancestor_seg=head_seg)
                steps += step_from_parent_map[destination]
            else:
                # p1 is some segment in between or the head of the quadrant
                steps += step_from_parent_map[current] - 1
                steps += count_steps_until_entering_the_ancestor(
                    head_seg, ancestor_seg=p1)
                steps += 1
                steps += count_steps_until_entering_the_ancestor(
                    dest_seg, ancestor_seg=p1)
                steps += step_from_parent_map[destination]

    return steps
