import numpy as np
from fractions import Fraction
from collections import namedtuple

Ray = namedtuple('Ray', ['slope', 'x_sign'])
# Ray.slope: a Fraction or '+inf' or '-inf'
# Ray.x_sign: 1 or -1 or 0, indicating the positive, negative or zero of the x
#             component of the ray. If `x_sign` == 0, only '+inf' or '-inf' of
#             the `slope` is allowed.

def load_asteroids(filename='day10-input.txt'):
    def fine_all_char(s, char):
        sub_string = s
        ind = 0
        ret = []
        while True:
            delta = sub_string.find('#')
            if delta == -1:
                break
            ind += delta
            ret.append(ind)

            sub_string = sub_string[delta+1:]
            ind += 1
        return ret

    with open(filename, 'r') as f:
        y = 0
        asteroids = []
        while True:
            line = f.readline()
            print(line.rstrip('\n'))
            if line == '':
                break

            for x in fine_all_char(line, '#'):
                asteroids.append( (x,y) )
            y += 1
    return asteroids

def make_ray(dx,dy):
    if dx == dy == 0:
        ret = None
    elif dx == 0:
        ret = Ray('+inf', 0) if dy > 0 else Ray('-inf', 0)
    else:
        slope = Fraction(int(dy),int(dx))
        ret = Ray(slope, 1) if dx > 0 else Ray(slope, -1)
    return ret

# coordinates = np.array(load_asteroids('day10-test0.txt'))
coordinates = np.array(load_asteroids())

import sys
if sys.argv[1] == '1':
    # Part 1
    n_observable = []
    for coord in coordinates:
        rays = set()
        diffs = coordinates - coord
        for dx,dy in diffs:
            ray = make_ray(dx,dy)
            if ray is not None:
                rays.add( ray )
        n_observable.append(len(rays))
    print(n_observable)
    max_value = np.max(n_observable)
    ind_max = np.argmax(n_observable)
    print(max_value)
    print(ind_max)

