import itertools
from intcode import IntcodeComputer, RunState
import pickle

def display_stdout(comp):
    while True:
        s = comp.stdout
        if s == None:
            break
        print(chr(s),end='')
    print('')


def test_combination(getter, comp):
    item_list = [
        # 'asterisk',
        # 'antenna',
        'easter egg',
        # 'jam',
        'space heater',
        'festive hat',
        'fixed point',
    ]
    hold = []

    def cases():
        for n_chosen in range(1,4):
            for items in itertools.combinations(item_list, n_chosen):
                yield items

    for items in cases():
        i = getter()
        if i == 'q':
            break
        elif i == 'i':
            comp.stdin = [ord(c) for c in 'inv\n']
            comp.run()
            display_stdout(comp)
            i = getter()

        # drop previously picked items
        for hold_item in hold:
            comp.stdin = [ord(c) for c in 'drop '+hold_item+'\n']
        hold = []

        # pick up items
        for item in items:
            comp.stdin = [ord(c) for c in 'take '+item+'\n']
            hold.append(item)

        # move to test
        comp.stdin = [ord(c) for c in 'west\n']

        comp.run()
        display_stdout(comp)


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
            display_stdout(comp)

        if comp._state == RunState.FINISHED:
            i = input('To reload? (y/n)')
            if i == 'n':
                break
            else:
                comp = pickle.load(open('day25_save.pickle', 'rb'))
