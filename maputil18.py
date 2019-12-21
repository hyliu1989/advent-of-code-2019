import numpy as np
from pylab import imshow, show, figure, pause
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
    def __init__(self, parent, segment:np.ndarray, children:list, length:int):
        self.parent = parent
        self.segment = segment
        self.children = children
        self.ordered_items = []  # (item_id, nth_tile_in_the_segment)
        self.length = length


def parse(c):
    if c == '#':
        return -999
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


## Build segment map and locate items
segment_map = np.empty(init_map.shape, object)
wall = -999
item_positions = {}

def make_segment_recursive(parent, pos, prev_move)-> Segment:
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
        trace_heads = explore(pos, prev_move)
        num = len(trace_heads)
        if num == 0:
            # finalize the Segment
            ret = Segment(parent, segment, [], collected_items, nth_tile)
            segment_map[ret.segment!=0] = ret
            break
        elif num == 1:
            # continue
            pos, prev_move = trace_heads[0]
        elif num >= 2:
            # finalize the Segment and start new searches
            ret = Segment(parent, segment, [], collected_items, nth_tile)
            segment_map[ret.segment!=0] = ret
            for i in range(num):
                pos, prev_move = trace_heads[i]
                ret.children.append(
                    make_segment_recursive(ret, pos, prev_move)
                )
            return ret


quadrants = [None] * 4
quadrants[0] = [make_segment_recursive(0, np.array([39,42]), Direction.EAST),
                make_segment_recursive(0, np.array([38,41]), Direction.NORTH),]

quadrants[1] = [make_segment_recursive(1, np.array([38,39]), Direction.NORTH),
                make_segment_recursive(1, np.array([39,38]), Direction.WEST),]

quadrants[2] = [make_segment_recursive(2, np.array([41,38]), Direction.WEST),
                make_segment_recursive(2, np.array([42,39]), Direction.SOUTH),]

quadrants[3] = [make_segment_recursive(3, np.array([42,41]), Direction.SOUTH),]


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


def find_reachable_keys(curr_map) -> list:
    pass
