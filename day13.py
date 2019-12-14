import numpy as np
from intcode import IntcodeComputer, RunState
import sys
from pylab import imshow, show, figure

with open('day13-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = IntcodeComputer(instr_list)

def update_canvas(comp, canvas):
    drawing_instruction = []
    comp.run()
    while True:
        ins = comp.get_stdout()
        if ins is None:
            break
        drawing_instruction.append(ins)
    
    
    for i in range(0,len(drawing_instruction), 3):
        x = drawing_instruction[i]
        y = drawing_instruction[i+1]
        t = drawing_instruction[i+2]
        if x == -1:
            print('current score:', t)
        else:
            canvas[y,x] = t
    return canvas


canvas = np.zeros((30,50), np.int8)
canvas = update_canvas(comp, canvas)
print(comp._state)

if sys.argv[1] == '1':
    print((canvas==2).sum())
else:
    print('current quaters:', comp._memory[0])
    comp._memory[0] = 2
    print('current quaters:', comp._memory[0])
    comp._mem_addr = 0
    comp._state = RunState.INIT

    ## Game I/O
    fh = figure()
    ah = fh.add_subplot(111)
    ih = ah.imshow(canvas)
    fh.show()
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

    print('Game start!')
    while True:
        canvas = update_canvas(comp, canvas)
        ih.set_data(canvas)
        fh.canvas.draw()
        i = getter()
        if i == 'a':
            comp.append_input(-1)
        elif i == 's':
            comp.append_input(0)
        elif i == 'd':
            comp.append_input(1)
        elif i == 'w':
            import pickle
            pickle.dump([comp, canvas], open('day13_save.pickle', 'wb'))

        if comp._state == RunState.FINISHED:
            i = input('To reload? (y/n)')
            if i == 'n':
                break
            else:
                import pickle
                comp, canvas = pickle.load(open('day13_save.pickle', 'rb'))

