import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause
import sys
from queue import Queue

with open('day23-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

instr_list = np.array(instr_list)

q = Queue()

computers = [IntcodeComputer(instr_list, input_list=(i,)) for i in range(50)]
for i in range(50):
    comp_obj = computers[i]
    comp_obj.run()

first_printed = False
NAT_data = None
NAT_data_prev_sent = None
while True:
    # collect the outputs
    for i in range(50):
        comp_obj = computers[i]
        addr = comp_obj.stdout
        while addr is not None:
            x = comp_obj.stdout
            y = comp_obj.stdout

            if addr == 255:
                # send to NAT
                if not first_printed:
                    print('x', x, 'y', y)
                    first_printed = True
                NAT_data = (x,y)
            else:
                q.put((addr,x,y))

            # prepare for next
            addr = comp_obj.stdout

    # feed the inputs
    sent = [False] * 50
    while not q.empty():
        addr, x, y = q.get()
        if addr < 50:
            computers[addr].stdin = (x,y)
            sent[addr] = True

    if np.any(sent) == False and NAT_data is not None:
        # NAT sends data to computer 0
        if NAT_data_prev_sent == NAT_data:
            print(NAT_data_prev_sent)
            break
        computers[0].stdin = NAT_data
        NAT_data_prev_sent = NAT_data
        sent[0] = True

    for i in range(50):
        if sent[i] is False:
            computers[i].stdin = -1
        computers[i].run()



