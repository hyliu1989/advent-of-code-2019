import numpy as np
import contexttimer
import sys
# part_id = int(sys.argv[1])
part_id = 0

# from intcode import IntcodeComputer, RunState
from direction import Direction, get_opposite, get_new_position, explore

class Segment:
    """Singly-connected segment

    A Segment does not have branches or forks. A Segment's head is inside
    the singly-connected segment while its inclusive tail can be the joint of
    a fork. Its ordered items are ordered according to the step to the maze
    center (fewest to most).

    """
    def __init__(self, parent, segment:np.ndarray, children:list,
                 ordered_items:list, length:int, quadrant:int):
        self.parent = parent
        self.segment = segment
        self.children = children
        self.ordered_items = ordered_items  # (item_id, nth_tile_in_the_segment)
        self.length = length
        self.quadrant = quadrant
        if parent in range(4):
            self.n_steps_to_before_quadrant_head = 0
        else:
            self.n_steps_to_before_quadrant_head = (
                parent.n_steps_to_before_quadrant_head + parent.length
            )

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

def _is_position_valid(pos):
    return init_map[tuple(pos)] != wall

## Build segment map and locate items
segment_map = np.empty(init_map.shape, object)
item_positions = {}

def _make_segment_recursive(parent, pos, prev_move, quadrant)-> Segment:
    # Segment init required variables
    segment = np.zeros_like(init_map, dtype=np.uint8)
    collected_items = []
    nth_tile = 0

    while True:
        nth_tile += 1
        ij = tuple(pos)
        segment[ij] = nth_tile
        item = init_map[ij]
        if item != 0:
            item_positions[item] = ij
            collected_items.append((item, nth_tile))
        trace_heads = explore(pos, prev_move, _is_position_valid)
        num = len(trace_heads)
        if num == 0:
            # finalize the Segment
            ret = Segment(parent, segment, [], collected_items, nth_tile, quadrant)
            segment_map[ret.segment!=0] = ret
            return ret
        elif num == 1:
            # continue
            pos, prev_move = trace_heads[0]
        elif num >= 2:
            # finalize the Segment and start new searches
            ret = Segment(parent, segment, [], collected_items, nth_tile, quadrant)
            segment_map[ret.segment!=0] = ret
            for i in range(num):
                pos, prev_move = trace_heads[i]
                ret.children.append(
                    _make_segment_recursive(ret, pos, prev_move, quadrant)
                )
            return ret


quadrants = [None] * 4
quadrants[0] = [_make_segment_recursive(0, np.array([39,42]), Direction.EAST,  0),
                _make_segment_recursive(0, np.array([38,41]), Direction.NORTH, 0),]

quadrants[1] = [_make_segment_recursive(1, np.array([38,39]), Direction.NORTH, 1),
                _make_segment_recursive(1, np.array([39,38]), Direction.WEST,  1),]

quadrants[2] = [_make_segment_recursive(2, np.array([41,38]), Direction.WEST,  2),
                _make_segment_recursive(2, np.array([42,39]), Direction.SOUTH, 2),]

quadrants[3] = [_make_segment_recursive(3, np.array([42,41]), Direction.SOUTH, 3),]


def _trim(segment):
    """trim out the branches that contains no keys"""
    to_remove = []
    branch_has_key = False
    for i,_ in segment.ordered_items:
        if 1 <= i <= 26:
            branch_has_key = True
            break

    for child in segment.children:
        child_has_key = _trim(child)
        if not child_has_key:
            to_remove.append(child)
        else:
            branch_has_key = True

    for child in to_remove:
        segment.children.remove(child)

    return branch_has_key


for quad in quadrants:
    for s in quad:
        _trim(s)
del quad, s

def visualize_trimmed():
    trimmed_map = np.zeros_like(init_map)
    def paint(s):
        trimmed_map[s.segment!=0] = 2
        for c in s.children:
            paint(c)
    for quad in quadrants:
        for s in quad:
            paint(s)

    for k in item_positions:
        if k > 0:
            i,j = item_positions[k]
            trimmed_map[i,j] = 1
    return trimmed_map


def find_common_parent(seg1, seg2):
    parent_list1 = [seg1]
    while True:
        p = parent_list1[-1].parent
        parent_list1.append(p)
        if p in range(4):
            break
    p = seg2
    have_common_parent = True
    while True:
        if p in parent_list1:
            break
        if p in range(4):
            have_common_parent = False
            break
        p = p.parent

    if have_common_parent:
        return p, None
    else:
        return parent_list1[-1], p


def count_steps_until_entering_the_ancestor(current_seg, *, ancestor_seg=None):
    step = 0
    p = current_seg.parent
    while True:
        if p == ancestor_seg or p in range(4):
            break
        step += p.length
        p = p.parent
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
        steps += dest_seg.segment[destination]
        steps += dest_seg.n_steps_to_before_quadrant_head
        assert (count_steps_until_entering_the_ancestor(dest_seg)
                == dest_seg.n_steps_to_before_quadrant_head)
        steps += 2
    else:
        head_seg = segment_map[current]
        if head_seg.quadrant != dest_seg.quadrant:
            # head and the key are in different quadrants
            steps += head_seg.segment[current]-1
            steps += head_seg.n_steps_to_before_quadrant_head
            if (head_seg.quadrant, dest_seg.quadrant) in [(0,2), (2,0), (1,3), (3,1)]:
                steps += 5
            else:
                steps += 3
            steps += dest_seg.n_steps_to_before_quadrant_head
            steps += dest_seg.segment[destination]
        else:
            p1, p2 = find_common_parent(head_seg, dest_seg)
            assert p2 is None
            # head and the key are in the same quadrant
            if p1 is dest_seg:
                steps += head_seg.segment[current] - 1
                steps += count_steps_until_entering_the_ancestor(
                    head_seg, ancestor_seg=dest_seg)
                steps += dest_seg.length - dest_seg.segment[destination] + 1
            elif p1 is head_seg:
                steps += head_seg.length - head_seg.segment[current]
                steps += count_steps_until_entering_the_ancestor(
                    dest_seg, ancestor_seg=head_seg)
                steps += dest_seg.segment[destination]
            else:
                # p1 is some segment in between or the head of the quadrant
                steps += head_seg.segment[current] - 1
                steps += count_steps_until_entering_the_ancestor(
                    head_seg, ancestor_seg=p1)
                steps += 1
                steps += count_steps_until_entering_the_ancestor(
                    dest_seg, ancestor_seg=p1)
                steps += dest_seg.segment[destination]

    return steps
