from intcode import IntcodeComputer
import itertools

# test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
# phase_seq = [4,3,2,1,0]
## expected output: 43210

# test_program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
#     101,5,23,23,1,24,23,23,4,23,99,0,0]
# phase_seq = [0,1,2,3,4]
## expected output: 54321

# test_program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
#     1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
# phase_seq = [1,0,4,3,2]
## expected output: 65210

with open('day07-input.txt') as f:
    test_program = [int(s) for s in f.readline().split(',')]

max_output = 0
max_phase_seq = None
for phase_seq in itertools.permutations(range(5)): 
    input = 0
    for phase in phase_seq:
        computer = IntcodeComputer(test_program, input_list=[phase, input])
        output = computer.run()
        input = output[0]
    if output[0] > max_output:
        max_output = output[0]
        max_phase_seq = phase_seq
print(max_output)
print(max_phase_seq)
