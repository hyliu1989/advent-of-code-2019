import numpy as np

with open('day08-input.txt') as f:
    input_str = f.readline()
    input_str = input_str.rstrip('\n')  

assert len(input_str) % (6*25) == 0
shape = (len(input_str)//(6*25), 6, 25)
array = np.zeros(len(input_str), np.uint8)
for i, c in enumerate(input_str):
    array[i] = int(c)
array.shape = shape
# print(array)

ind_layer = np.argmin(np.sum(array==0, axis=(1,2)))

n_digit_one = (array[ind_layer] == 1).sum()
n_digit_two = (array[ind_layer] == 2).sum()
print('Part 1', n_digit_one*n_digit_two)


# Part 2
result = array[0]
for i in range(1,shape[0]):
    transparent = result == 2
    result[transparent] = array[i][transparent]

print(result)
