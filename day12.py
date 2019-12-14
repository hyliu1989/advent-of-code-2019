import numpy as np
import itertools
import sys

class Moon:
    def __init__(self, x,y,z):
        self.position = np.array([x,y,z], np.int64)
        self.velocity = np.array([0,0,0], np.int64)

    def copy(self):
        ret = Moon(*self.position)
        ret.velocity = self.velocity.copy()
        return ret

    def __repr__(self):
        return ('\n<class Moon object position=[%d,%d,%d] velocity=[%d,%d,%d]>'
                % (tuple(self.position) + tuple(self.velocity)))

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
    # instead of bruteforce looking for it, let's peek the behavior
    moon_list_for_x = [m.copy() for m in moon_list]
    moon_list_for_y = [m.copy() for m in moon_list]
    moon_list_for_z = [m.copy() for m in moon_list]

    moon_lists = [moon_list_for_x, moon_list_for_y, moon_list_for_z]
    required_steps = []

    for i in range(3):
        current_list = moon_lists[i]
        step = 0
        history = {}
        def build_state(moon_list):
            state = ()
            for m in moon_list:
                state += (m.position[i], m.velocity[i])
            return state

        state = build_state(current_list)
        history[state] = True

        while True:
            # Proceed to a new state
            proceed_1(current_list)
            step += 1

            # Check the currently proceeded state
            state = build_state(current_list)
            if history.get(state) is not None:
                break
            else:
                history[state] = True

            if step % 100000 == 0:
                print('step', step)
        
        required_steps.append(step)

    import math
    def lcm(x,y):
        return x*y//math.gcd(x,y)

    print(required_steps)
    print(lcm(lcm(required_steps[0], required_steps[1]), required_steps[2]))