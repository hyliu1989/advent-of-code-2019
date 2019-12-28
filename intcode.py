import numpy as np
from enum import IntEnum

class Opcode(IntEnum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    ADJUST_BASE = 9
    TERMINATE = 99

class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

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
        Opcode.ADJUST_BASE: 1,
        Opcode.TERMINATE: 1,
    }
    OPERATION_OF_OPCODE = {}

    def __init__(self, instruction_list, input_list=None):
        self._state = RunState.INIT

        self._memory = np.zeros(2**16, dtype=np.int64)
        self._mem_addr = 0
        self._memory[:len(instruction_list)] = instruction_list

        self._relative_base = 0

        self._input_list = [] if input_list is None else [i for i in input_list]
        self._input_addr = 0

        self._output_list = []
        self._output_addr = 0

    @property
    def state(self):
        return self._state

    def append_input(self, item):
        self.stdin = item

    def get_stdout(self):
        return self.stdout

    @property
    def stdin(self):
        raise RuntimeError('stdin is not readable')
        return None

    @stdin.setter
    def stdin(self, x):
        if hasattr(x, '__iter__'):
            for xx in x:
                self._input_list.append(xx)
        else:
            self._input_list.append(x)

    @property
    def stdout(self):
        if self._output_addr == len(self._output_list):
            return None
        else:
            ret = self._output_list[self._output_addr]
            self._output_addr += 1
            return ret

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
            elif opcode == Opcode.ADJUST_BASE:
                already_moved = self._op_adjust_base(params, param_modes)
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
        """Parse the instruction and return the opcode and parameter modes

        opcode stands for operation code and is the 2 right-most digits.
        parameters for the inputs of that operation is the continuing digits
        from the above 2, from right to left. E.g. hundreds are for the first
        parameter, thousands are for the second parameter, ten thousands are
        for the third, ....

        """
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

        raw_params is from the _memory and should not be altered!
        param_modes is temporary for current process and can be changed.

        """
        output_addr = None
        if index_of_output_addr is not None:
            i = index_of_output_addr
            # Output should use POSITION or RELATIVE modes to indicate the addr
            # to write to.
            assert param_modes[i] != ParamMode.IMMEDIATE

            # Compute the parameter RELATIVE mode output
            p = raw_params[i]
            if param_modes[i] == ParamMode.POSITION:
                output_addr = p
            elif param_modes[i] == ParamMode.RELATIVE:
                output_addr = self._relative_base + p

            # make it IMMEDIATE so it just appends the parameter to ret
            param_modes[i] = ParamMode.IMMEDIATE

        ret = []
        for p, m in zip(raw_params, param_modes):
            if m == ParamMode.POSITION:
                ret.append(self._memory[p])
            elif m == ParamMode.IMMEDIATE:
                ret.append(p)
            elif m == ParamMode.RELATIVE:
                addr = self._relative_base + p
                assert addr >= 0
                ret.append(self._memory[addr])
            else:
                raise ValueError()

        # put the output address back
        if output_addr is not None:
            ret[index_of_output_addr] = output_addr

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


    def _op_adjust_base(self, params, param_modes):
        adj, = self._fetch_params(params, param_modes)
        self._relative_base += adj


    def _op_terminate(self, params, param_modes):
        self._state = RunState.FINISHED




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
