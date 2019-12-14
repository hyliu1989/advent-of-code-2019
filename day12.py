import numpy as np
import itertools
import sys

class Moon:
    def __init__(self, x,y,z):
        self.position = np.array([x,y,z], np.int64)
        self.velocity = np.array([0,0,0], np.int64)

    def interact(self, moon):
        diff = self.position - moon.position
        self.velocity[diff > 0] -= 1
        moon.velocity[diff > 0] += 1

        self.velocity[diff < 0] += 1
        moon.velocity[diff < 0] -= 1

    def step(self):
        self.position += self.velocity

    @property
    def energy(self):
        return abs(self.position).sum() * abs(self.velocity).sum()
    

def proceed_1(moon_list):
    # apply gravity
    for i1, i2 in itertools.combinations(range(len(moon_list)),2):
        m1, m2 = moon_list[i1], moon_list[i2]
        m1.interact(m2)

    # apply velocity
    for m in moon_list:
        m.step()


# Test
if sys.argv[1] == '0':
    moon_list = [
        Moon(-1,0,2),
        Moon(2,-10,-7),
        Moon(4,-8,8),
        Moon(3,5,-1),
    ]
    n_steps = 10
    debug = True

elif sys.argv[1] == '1':
    moon_list = [
        Moon( -9, -1, -1),
        Moon(  2,  9,  5),
        Moon( 10, 18,-12),
        Moon( -6, 15, -7),
    ]
    n_steps = 1000
    debug = False

elif sys.argv[1] == '2':
    moon_list = [
        Moon( -9, -1, -1),
        Moon(  2,  9,  5),
        Moon( 10, 18,-12),
        Moon( -6, 15, -7),
    ]


if sys.argv[1] in ['0', '1']:
    for _ in range(n_steps):
        proceed_1(moon_list)

        if debug:
            for m in moon_list:
                print(m.position, m.velocity)
            print('===========')

    energy = 0
    for m in moon_list:
        energy += m.energy
    print('energy', energy)

else:
    def build_state(moon_list):
        ret = ()
        for m in moon_list:
            ret += tuple(m.position) + tuple(m.velocity)
        return ret

    state = build_state(moon_list)
    history = {}
    history[state] = True
    step = 0
    while True:
        # Proceed to a new state
        proceed_1(moon_list)
        step += 1

        # Check the currently proceeded state
        state = build_state(moon_list)
        if history.get(state) is not None:
            break
        else:
            history[state] = True

        if step % 1000000 == 0:
            print('step', step)

    print(step)