import numpy as np
from intcode import IntcodeComputer, RunState
import sys
from pylab import imshow, show, figure
import pickle

with open('day25-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = IntcodeComputer(instr_list)
print(comp._state)


class _GetchUnix:
    # https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
getter = _GetchUnix()

def run_game(getter, comp):
    print('Game start!')
    while True:
        i = getter()
        to_run = True
        if i == 'a':
            comp.stdin = [ord(c) for c in 'west\n']
        elif i == 's':
            comp.stdin = [ord(c) for c in 'south\n']
        elif i == 'd':
            comp.stdin = [ord(c) for c in 'east\n']
        elif i == 'w':
            comp.stdin = [ord(c) for c in 'north\n']
        elif i == 't':
            s = input('take: ')
            comp.stdin = [ord(c) for c in 'take '+s+'\n']
        elif i == 'y':
            s = input('drop: ')
            comp.stdin = [ord(c) for c in 'drop '+s+'\n']
        elif i == 'i':
            comp.stdin = [ord(c) for c in 'inv\n']
        elif i == 'r':
            s = input('raw input: ')
            comp.stdin = [ord(c) for c in s+'\n']
        elif i == 'q':
            break
        elif i == 'z':
            to_run = False
            pickle.dump(comp, open('day25_save.pickle', 'wb'))
        elif i == 'x':
            to_run = False
            comp = pickle.load(open('day25_save.pickle', 'rb'))

        if to_run:
            comp.run()

            while True:
                s = comp.stdout
                if s == None:
                    break
                print(chr(s),end='')
            print('')

        if comp._state == RunState.FINISHED:
            i = input('To reload? (y/n)')
            if i == 'n':
                break
            else:
                comp = pickle.load(open('day25_save.pickle', 'rb'))

