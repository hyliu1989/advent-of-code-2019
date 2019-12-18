import numpy as np
# from intcode import IntcodeComputer, RunState
# from pylab import imshow, show, figure, pause
import contexttimer
import sys
part_id = int(sys.argv[1])
# part_id = 0

with open('day16-input.txt', 'r') as f:
    input_signal = np.array([int(w) for w in f.readline() if w != '\n'], dtype=np.int64)

# input_signal = np.array([1,2,3,4,5,6,7,8])

def compute(input_signal, n_phase, output_offset=0):
    for phase in range(1,n_phase+1):
        output_signal = np.zeros_like(input_signal)
        for i in range(len(input_signal)):
            repeating_pattern = (np.array([0,1,0,-1])[:,np.newaxis] + np.zeros(i+1)).ravel()
            rep_times = int(np.ceil((input_signal.size+1) / repeating_pattern.size))
            to_multiply = (repeating_pattern[np.newaxis,:] + np.zeros((rep_times,1))).ravel()
            to_multiply = to_multiply[1:1+input_signal.size]
            product = (input_signal * to_multiply).sum()
            output_signal[i] = abs(product) % 10

        input_signal = output_signal

    return output_signal[output_offset:output_offset+8]

## New method
def _FFT(x):
    y = np.zeros_like(x)
    bands_pos = range(1, x.size, 4)
    bands_neg = range(3, x.size, 4)
    
    for band_head in bands_pos:
        # initialize for the first output element
        ind_output = 0
        band_sum = x[band_head]
        start = band_head
        stop = band_head + 1
        y[ind_output] += band_sum

        for ind_output in range(1, y.size):
            new_start = band_head * (ind_output+1)
            if new_start >= y.size:
                break
            new_stop = (band_head + 1) * (ind_output+1)
            band_sum -= x[start:min(stop,new_start)].sum()
            band_sum += x[max(stop,new_start):new_stop].sum()
            start = new_start
            stop = new_stop
            y[ind_output] += band_sum

    for band_head in bands_neg:
        # initialize for the first output element
        ind_output = 0
        band_sum = x[band_head]
        start = band_head
        stop = band_head + 1
        y[ind_output] -= band_sum

        for ind_output in range(1, y.size):
            new_start = band_head * (ind_output+1)
            if new_start >= y.size:
                break
            new_stop = (band_head + 1) * (ind_output+1)
            band_sum -= x[start:min(stop,new_start)].sum()
            band_sum += x[max(stop,new_start):new_stop].sum()
            start = new_start
            stop = new_stop
            y[ind_output] -= band_sum
    return y

def fft(x):
    # n = 2 ** int(np.ceil(np.log2(x.size+1)))
    n = 1+x.size
    x_prime = np.zeros(n, np.int64)
    x_prime[1:1+x.size] = x
    y_prime = _FFT(x_prime)
    y = abs(y_prime[:x.size]) % 10
    return y

if part_id == 0:
    def print_weights(length):
        l = length
        for i in range(1,1+length):
            pattern = '0'*i + '1'*i + '0'*i + '#'*i
            rep = int(np.ceil(l / len(pattern)))
            print((pattern*rep)[:length])
    print_weights(80)


if part_id == 1:
    with contexttimer.Timer() as t:
        print(compute(input_signal, n_phase=100))
    print('time:', t.elapsed)

    with contexttimer.Timer() as t:
        for phase in range(100):
            input_signal = fft(input_signal)
        print(input_signal[:8])
    print('time:', t.elapsed)

if part_id == 2:
    input_signal = np.array([int(s) for s in '03036732577212944063491565474664'])
    input_signal2 = (input_signal + np.zeros((10000,1))).ravel()
    offset = 0
    for n in input_signal[:7]:
        offset += n
        offset *= 10
    offset //= 10
    print(offset, input_signal2[:7])

    with contexttimer.Timer() as t:
        for phase in range(100):
            input_signal2 = fft(input_signal2)
    print(input_signal2[offset:offset+8])
    print('time:', t.elapsed)
