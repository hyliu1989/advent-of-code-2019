from intcode import IntcodeComputer, RunState
import itertools


with open('day07-input.txt') as f:
    test_program = [int(s) for s in f.readline().split(',')]

max_output = 0
max_phase_seq = None
for phase_seq in itertools.permutations(range(5,10)): 
    # setup the computer phase
    list_computers = [IntcodeComputer(test_program, input_list=[phase])
                      for phase in phase_seq]

    # start running
    list_computers[0].append_input(0)
    kick_off = True
    to_terminate = False
    while not to_terminate:
        for i in range(5):
            curr_computer = list_computers[i]
            prev_computer = list_computers[i-1]

            if kick_off:
                kick_off = False
                curr_computer.run()
            else:
                if curr_computer.state == RunState.FINISHED:
                    to_terminate = True
                    assert i == 0
                    break
                curr_input = prev_computer.get_stdout()
                assert curr_input is not None
                curr_computer.append_input(curr_input)
                curr_computer.run()
    output = list_computers[4].get_stdout()
    assert list_computers[4].get_stdout() is None
    if output > max_output:
        max_output = output
        max_phase_seq = phase_seq
print(max_output)
print(max_phase_seq)
