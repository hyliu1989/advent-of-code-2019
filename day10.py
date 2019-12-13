import numpy as np
from fractions import Fraction


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

def make_angle(dx,dy):
    # pointing north is zero degree and increase clock wise
    if dx == dy == 0:
        angle = None
    elif dx == 0:
        angle = np.pi if dy > 0 else 0.0
    else:
        slope = float(Fraction(int(dy),int(dx)))
        angle = np.arctan(slope) + np.pi/2
        if dx < 0:
            angle += np.pi
    return angle

# coordinates = np.array(load_asteroids('day10-test0.txt'))
coordinates = np.array(load_asteroids())

import sys
if sys.argv[1] == '1':
    # Part 1
    n_observable = []
    for coord in coordinates:
        angles = set()
        diffs = coordinates - coord
        for dx,dy in diffs:
            angle = make_angle(dx,dy)
            if angle is not None:
                angles.add( angle )
        n_observable.append(len(angles))
    print(n_observable)
    max_value = np.max(n_observable)
    ind_max = np.argmax(n_observable)
    print(max_value)
    print(ind_max)

elif sys.argv[1] == '2':
    # Part 2
    max_value = 274
    ind_max = 210
    coord = coordinates[ind_max]
    diffs = coordinates - coord

    # sort into angle basckets
    angle_baskets = {}
    for dx,dy in diffs:
        angle = make_angle(dx,dy)
        if angle is not None:
            points_with_same_angle = angle_baskets.get(angle)
            if points_with_same_angle is None:
                points_with_same_angle = []
                angle_baskets[angle] = points_with_same_angle
            points_with_same_angle.append((dx,dy, dx**2+dy**2))

    # sort keys
    sorted_keys = sorted(angle_baskets.keys())

    # sort each basket
    for k in sorted_keys:
        points_with_same_angle = np.array(angle_baskets[k])
        distances = points_with_same_angle[:,2]
        sorting_indexes = np.lexsort(keys=[distances,])
        angle_baskets[k] = points_with_same_angle[sorting_indexes,:2]
        angle_baskets[k] = list(angle_baskets[k])

    # find the asteroid
    count = 0
    while count < 200:
        for k in sorted_keys:
            if len(angle_baskets[k]) != 0:
                dx,dy = angle_baskets[k].pop(0)
                count += 1
                if count == 200:
                    break
    print(coord[0] + dx, coord[1] + dy)
