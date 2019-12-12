import numpy as np

def calc_total_fuel(mass):
    current_fuel = int(np.floor(mass/3))-2
    if current_fuel <= 0:
        total_fuel = 0
    else:
        total_fuel = current_fuel + calc_total_fuel(current_fuel)

    return total_fuel

if __name__ == '__main__':
    sum = 0
    with open('day01-1.txt', 'r') as f:
        while True:
            s = f.readline()
            if s == '':
                break
            sum += calc_total_fuel(int(s))
    print(sum)