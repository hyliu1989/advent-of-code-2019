import intcode

with open('day09-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]

comp = intcode.IntcodeComputer(instr_list, [1,])
print('Part 1', comp.run())


comp = intcode.IntcodeComputer(instr_list, [2,])
print('Part 2', comp.run())
