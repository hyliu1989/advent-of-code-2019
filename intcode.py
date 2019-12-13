import numpy as np
from enum import IntEnum

def run_instruction_list(instruction_list, noun=12, verb=2, verbose=True):
    """Intcode computer from day 2 challenge
    """
    instruction_list = list(instruction_list)
    instruction_list[1] = noun
    instruction_list[2] = verb
    total_len = len(instruction_list)

    count = 0
    instr_pointer = 0
    while True:
        if instr_pointer >= total_len:
            print('error: reach the end without encountering 99')
            break

        instr = instruction_list[instr_pointer]

        # instruction 99
        if instr == 99:
            num_value_of_instr = 1
            instr_pointer += num_value_of_instr
            if verbose:
                print('finished!')
            break

        # instructions 1 (addition) and 2 (multiplication)
        if instr_pointer+3 >= total_len:
            print('error: reach the end without encountering 99')
            break
        i1,i2,i3 = instruction_list[instr_pointer+1:instr_pointer+4]
        num_value_of_instr = 4
        number1, number2 = instruction_list[i1], instruction_list[i2]
        if instr == 1:
            instruction_list[i3] = number1 + number2
        elif instr == 2:
            instruction_list[i3] = number1 * number2
        else:
            print('error: unknown instruction_list')
            break

        instr_pointer += num_value_of_instr
    return instruction_list



class Opcode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    TERMINATE = 99

class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

class RunState(IntEnum):
    INIT = 0
    RUNNING = 1
    PAUSED = 2
    FINISHED = 3

class IntcodeComputer():
    NUM_PARAMS_OF_OPCODE = {
        Opcode.ADD: 3,
        Opcode.MULTIPLY: 3,
        Opcode.INPUT: 1,
        Opcode.OUTPUT: 1,
        Opcode.JUMP_IF_TRUE: 2,
        Opcode.JUMP_IF_FALSE: 2,
        Opcode.LESS_THAN: 3,
        Opcode.EQUAL: 3,
        Opcode.TERMINATE: 1,
    }
    OPERATION_OF_OPCODE = {}

    def __init__(self, instruction_list, input_list=None):
        self._state = RunState.INIT

        self._memory = np.array(instruction_list)
        self._mem_addr = 0

        self._input_list = input_list
        self._input_addr = 0

        self._output_list = []


    @property
    def state(self):
        return self._state

    def append_input(self, item):
        self._input_list.append(item)

    @property
    def outputs(self):
        return self._output_list.copy()


    def run(self):
        # Check it is not terminated
        assert self._state != RunState.FINISHED

        # Start running
        self._state = RunState.RUNNING
        while self._state not in [RunState.FINISHED, RunState.PAUSED]:
            opcode, param_modes = self._parse_one_instruction(
                self._memory[self._mem_addr]
            )
            num_param = len(param_modes)
            params = self._memory[self._mem_addr+1:self._mem_addr+1+num_param]
            # Check the opcode and determine which function to call
            if   opcode == Opcode.ADD:
                already_moved = self._op_add(params, param_modes)
            elif opcode == Opcode.MULTIPLY:
                already_moved = self._op_multiply(params, param_modes)
            elif opcode == Opcode.INPUT:
                already_moved = self._op_stdin(params, param_modes)
            elif opcode == Opcode.OUTPUT:
                already_moved = self._op_stdout(params, param_modes)
            elif opcode == Opcode.JUMP_IF_TRUE:
                already_moved = self._op_jump_if_true(params, param_modes)
            elif opcode == Opcode.JUMP_IF_FALSE:
                already_moved = self._op_jump_if_false(params, param_modes)
            elif opcode == Opcode.LESS_THAN:
                already_moved = self._op_less_than(params, param_modes)
            elif opcode == Opcode.EQUAL:
                already_moved = self._op_equal(params, param_modes)
            elif opcode == Opcode.TERMINATE:
                already_moved = self._op_terminate(params, param_modes)
            else:
                raise ValueError('Unknown opcode %d' % opcode)

            if self._state == RunState.PAUSED:
                return

            # move the memory pointer
            if not already_moved:
                step = self.NUM_PARAMS_OF_OPCODE[opcode] + 1
                self._mem_addr += step
        return self._output_list.copy()


    @classmethod
    def _parse_one_instruction(cls, instr):
        opcode = Opcode(instr % 100)
        instr //= 100  # get rid of the opcode
        num_param = cls.NUM_PARAMS_OF_OPCODE[opcode]
        parameter_modes = []
        for i in range(num_param):
            parameter_modes.append(ParamMode(instr % 10))
            instr //= 10
        return opcode, parameter_modes


    def _fetch_params(self, raw_params, param_modes, index_of_output_addr=None):
        """Fetch the parameters based on the parameter modes
        """
        if index_of_output_addr is not None:
            i = index_of_output_addr
            assert param_modes[i] == ParamMode.POSITION
            param_modes[i] = ParamMode.IMMEDIATE # make it IMMEDIATE so we get
                                                 # the raw value as the addr
        ret = []
        for p, m in zip(raw_params, param_modes):
            if m == ParamMode.POSITION:
                ret.append(self._memory[p])
            elif m == ParamMode.IMMEDIATE:
                ret.append(p)
            else:
                raise ValueError()
        return ret


    def _op_add(self, params, param_modes):
        int1, int2, save_addr = self._fetch_params(params, param_modes,
                                                   index_of_output_addr=2)
        self._memory[save_addr] = int1 + int2


    def _op_multiply(self, params, param_modes):
        int1, int2, save_addr = self._fetch_params(params, param_modes,
                                                   index_of_output_addr=2)
        self._memory[save_addr] = int1 * int2


    def _op_stdin(self, params, param_modes):
        # if input_addr is at the end of the list, pause
        if self._input_addr == len(self._input_list):
            self._state = RunState.PAUSED
            return

        save_addr, = self._fetch_params(params, param_modes,
                                        index_of_output_addr=0)
        self._memory[save_addr] = self._input_list[self._input_addr]
        self._input_addr += 1


    def _op_stdout(self, params, param_modes):
        to_output, = self._fetch_params(params, param_modes)

        self._output_list.append(to_output)


    def _op_jump_if_true(self, params, param_modes):
        condition, new_mem_addr = self._fetch_params(params, param_modes)

        if condition != 0:
            self._mem_addr = new_mem_addr
            return True
        else:
            return False


    def _op_jump_if_false(self, params, param_modes):
        condition, new_mem_addr = self._fetch_params(params, param_modes)

        if condition == 0:
            self._mem_addr = new_mem_addr
            return True
        else:
            return False


    def _op_less_than(self, params, param_modes):
        i1, i2, save_addr = self._fetch_params(params, param_modes,
                                               index_of_output_addr=2)
        self._memory[save_addr] = 1 if i1 < i2 else 0


    def _op_equal(self, params, param_modes):
        i1, i2, save_addr = self._fetch_params(params, param_modes,
                                               index_of_output_addr=2)
        self._memory[save_addr] = 1 if i1 == i2 else 0


    def _op_terminate(self, params, param_modes):
        self._state = RunState.FINISHED
