import intcode

# Part 1
with open('day05-input.txt', 'r') as f:
    instr_list = [int(w) for w in f.readline().split(',')]


print('============== Part 1 ==============')
comp = intcode.IntcodeComputer(instr_list, input_list=[1,])
print(comp.run())


print('============== Part 2 ==============')
print('test')
instr_list_test_0 = [
    3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
comp = intcode.IntcodeComputer(instr_list_test_0, input_list=[7,])
print(comp.run(), 'expect 999')

comp = intcode.IntcodeComputer(instr_list_test_0, input_list=[8,])
print(comp.run(), 'expect 1000')

comp = intcode.IntcodeComputer(instr_list_test_0, input_list=[9,])
print(comp.run(), 'expect 1001')


print('quest')
comp = intcode.IntcodeComputer(instr_list, input_list=[5,])
print(comp.run())
