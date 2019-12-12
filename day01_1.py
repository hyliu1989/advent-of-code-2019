import numpy as np

def calc_fuel(mass):
    return int(np.floor(mass/3))-2

if __name__ == '__main__':
    sum = 0
    with open('day01-1.txt', 'r') as f:
        while True:
            s = f.readline()
            if s == '':
                break
            sum += calc_fuel(int(s))
    print(sum)