import numpy as np
from intcode import IntcodeComputer, RunState
from pylab import imshow, show, figure, pause

with open('day19-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]


res = np.zeros((50,50), np.bool)
for i in range(50):
    for j in range(50):
        comp = IntcodeComputer(instr_list)
        comp.stdin = (j,i)
        comp.run()
        res[i,j] = comp.stdout


