class CelestialObject:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self._n_direct_orbits = None
        self._n_indirect_orbits = None

    @property
    def n_direct_orbits(self):
        if self._n_direct_orbits is None:
            self._n_direct_orbits = 0 if self.parent is None else 1
        return self._n_direct_orbits

    @property
    def n_indirect_orbits(self):
        if self._n_indirect_orbits is None:
            if self.parent is None:
                self._n_indirect_orbits = 0
            else:
                self._n_indirect_orbits = (self.parent.n_direct_orbits
                                           + self.parent.n_indirect_orbits)
        return self._n_indirect_orbits

celes_dict = {}

# Link the connection
with open('day06-input.txt') as f:
    while True:
        s = f.readline()
        if s == '':
            break
        s = s.rstrip('\n')

        parent_name, child_name = s.split(')')
        parent = celes_dict.get(parent_name)
        child = celes_dict.get(child_name)

        if parent is None:
            parent = CelestialObject(parent_name, None)
            celes_dict[parent_name] = parent
        else:
            pass

        assert parent is not None
        if child is None:
            child = CelestialObject(child_name, parent)
            celes_dict[child_name] = child
        else:
            assert child.parent is None
            child.parent = parent

for k in celes_dict:
    assert celes_dict[k].parent is not None or k == 'COM', k

total = 0
for k in celes_dict:
    obj = celes_dict[k]
    total += obj.n_direct_orbits + obj.n_indirect_orbits
print('Part 1', total)


# Part 2
YOU = celes_dict['YOU']
SAN = celes_dict['SAN']

# build a trace
trace_YOU = set()
obj = YOU.parent
while obj is not None:
    trace_YOU.add(obj.name)
    obj = obj.parent
assert 'SAN' not in trace_YOU


intersection = None
obj = SAN.parent
n_trans_from_inter_to_SAN_parent = 0
while obj is not None:
    if obj.name in trace_YOU:
        intersection = obj
        break
    else:
        obj = obj.parent
        n_trans_from_inter_to_SAN_parent += 1
assert intersection is not None

n_trans_from_YOU_parent_to_inter = 0
obj = YOU.parent
while obj is not intersection:
    obj = obj.parent
    n_trans_from_YOU_parent_to_inter += 1

print('Part 2', n_trans_from_YOU_parent_to_inter 
                + n_trans_from_inter_to_SAN_parent)
