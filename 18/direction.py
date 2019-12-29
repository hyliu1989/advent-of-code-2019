from enum import IntEnum
from collections import namedtuple
import numpy
import numpy as np

StepTrace = namedtuple('StepTrace', ['pos', 'prev_move'])

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

    @classmethod
    def all(cls):
        return [cls.NORTH, cls.SOUTH, cls.WEST, cls.EAST]


_opposite = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST:  Direction.EAST,
    Direction.EAST:  Direction.WEST,
}


def get_opposite(x):
    return _opposite[x]


def get_new_position(pos:numpy.ndarray, direction:Direction):
    if   direction == Direction.NORTH:
        new_pos = pos - [1,0]
    elif direction == Direction.SOUTH:
        new_pos = pos + [1,0]
    elif direction == Direction.WEST:
        new_pos = pos - [0,1]
    elif direction == Direction.EAST:
        new_pos = pos + [0,1]
    return new_pos

def explore(pos, prev_move, is_position_valid):
    dir_to_explore = Direction.all()
    dir_to_explore.remove(get_opposite(prev_move))
    dir_to_explore = np.array(dir_to_explore)
    del prev_move

    trace_heads = []
    for i in range(3):
        direction = dir_to_explore[i]
        new_pos = get_new_position(pos, direction)
        if is_position_valid(new_pos):
            trace_heads.append(
                StepTrace(pos=new_pos, prev_move=direction)
            )
    return trace_heads
