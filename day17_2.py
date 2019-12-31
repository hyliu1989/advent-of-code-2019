import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day17-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]
instr_list = np.array(instr_list)
instr_list[0] = 2

comp = IntcodeComputer(instr_list)
comp.run()

def print_out(intcode_comp):
    while True:
        c = intcode_comp.stdout
        if c is not None:
            if c < 128:
                print(chr(c), end='')
            else:
                print('score:', c)
        else:
            break
print_out(comp)

"""
..............#####................................
..............#...#................................
....#############.#................................
....#.........#.#.#................................
#############.#######..............................
#...#.......#...#.#.#..............................
#...#.......#...#.#.#.....................#########
#...#.......#...#.#.#.....................#.......#
#####.......#...#.#.#.....................#.......#
............#...#.#.#.....................#.......#
....#############.#.#.....................#.......#
....#.......#.....#.#.....................#.......#
....#.#############.#.....................#.......#
....#.#.....#.......#.....................#.......#
....#.#.....#.....#############.......#############
....#.#.....#.....#.#.........#.......#...#........
....#.#.....#########.........#.......#...#........
....#.#...........#...........#.......#...#........
....#.#.#########.#...........#.......#...######^..
....#.#.#.......#.#...........#.......#............
....#.#############...........#.......#............
....#...#.......#.............#.......#............
....#####.......#.............#.......#............
................#.............#.......#............
................#.............#.......#............
................#.............#.......#............
................#.............#########............
................#..................................
................#..................................
................#..................................
................#############......................
"""
# L,6,R,12,R,8,R,8,R,12,L,12,R,8,R,12,L,12,L,6,R,12,R,8,R,
#                                                         12,L,12,L,4,L,4,L,6,R,12,R,8,R,12,      L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,R,8,R,12,L,12
#                                                         6,R,4,L,8,L,12,L,6,R,4,R,4,R,12,R,6,R,8,L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,R,8,R,12,L,12

# L,6,R,12,R,8,R,8,R,12,L,12,R,8,R,12,L,12,L,6,R,12,R,8,R,12,L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,L,6,R,12,R,8,R,12,L,12,L,4,L,4,R,8,R,12,L,12

main_routine = 'A,B,B,A,C,A,C,A,C,B'
func_A = 'L,6,R,12,R,8'
func_B = 'R,8,R,12,L,12'
func_C = 'R,12,L,12,L,4,L,4'
video_mode = 'n'
for instr in [main_routine, func_A, func_B, func_C, video_mode]:
    # assert len(instr) <= 20
    comp.stdin = [ord(c) for c in instr]
    comp.stdin = ord('\n')
    comp.run()
    print_out(comp)


print_out(comp)
