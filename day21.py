import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause
import sys

with open('day21-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = IntcodeComputer(instr_list)
out = comp.run()

def feed(s):
    for c in s:
        comp.append_input(ord(c))
    comp.run()
    ret = []
    while True:
        c = comp.get_stdout()
        if c != None:
            ret.append(c)
        else:
            break
    return ret

if sys.argv[1] == '1':
    res = feed("""OR A T
AND B T
AND C T
NOT T J
AND D J
WALK
""")

else:
    res = feed("""OR A T
AND B T
AND C T
NOT T J
AND D J
AND H J
NOT A T
OR T J
RUN
""")

print(''.join([chr(i) for i in res if i < 128]))
print(res[-1])
