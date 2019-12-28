import maputil18 as maputil
import numpy as np
from pylab import imshow, show, figure, pause
import heapq
Segment = maputil.Segment


class SearchTrace:
    min_step = np.inf
    @classmethod
    def get_min_step(cls):
        return cls.min_step

    @classmethod
    def set_min_step(cls, value):
        if cls.min_step > value:
            cls.min_step = value

    def __init__(self, to_init_search=False):
        self.reachable_keys = np.zeros(26+1, np.bool)
        self.blockers =  np.zeros(26*2+1, np.bool)
        self.collected_keys = np.zeros(26+1, np.bool)
        self.step = 0
        self.trace = []

        if to_init_search:
            self._initial_search()


    def __ge__(self, other):  return self.step >= other.step
    def __gt__(self, other):  return self.step >  other.step
    def __le__(self, other):  return self.step <= other.step
    def __lt__(self, other):  return self.step <  other.step
    def __eq__(self, other):  return self.step == other.step
    def __ne__(self, other):  return self.step != other.step


    def copy(self):
        ret = SearchTrace()
        ret.reachable_keys = self.reachable_keys.copy()
        ret.blockers = self.blockers.copy()
        ret.collected_keys = self.collected_keys.copy()
        ret.step = self.step
        ret.trace = self.trace.copy()
        return ret

    def pack(self):
        self.reachable_keys = np.packbits(self.reachable_keys)
        self.blockers = np.packbits(self.blockers)
        self.collected_keys = np.packbits(self.collected_keys)
        self.trace = np.array(self.trace, np.uint8)
        return self

    def unpack(self):
        self.reachable_keys = np.unpackbits(self.reachable_keys)[:27]
        self.blockers = np.unpackbits(self.blockers)[:26*2+1]
        self.collected_keys = np.unpackbits(self.collected_keys)[:27]
        self.trace = list(self.trace)
        return self

    def _initial_search(self):
        for quad in maputil.quadrants:
        # for quad in [maputil.quadrants[1][1:2]]:
            for seg in quad:
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blockers, self.collected_keys)

    def get_key(self, key):
        assert self.reachable_keys[key] == True

        # count the step to move to where the key is
        head_pos = maputil.item_positions[self.trace[-1]] if self.trace else (40,40)
        key_pos = maputil.item_positions[key]
        n_steps = maputil.move(head_pos, key_pos)
        self.step += n_steps

        self.reachable_keys[key] = False
        self.collected_keys[key] = True
        self.trace.append(key)
        obtained_key = key

        if self.step > self.get_min_step():
            return 'abort'

        # Check the removed blockers
        for item in range(-26,27):
            if not self.blockers[item] or item == 0:
                continue

            if abs(item) == obtained_key:  # this checks for both key and door
                # Remove the blocker from the list
                self.blockers[item] = False
                # Recursively search
                blocker_pos = maputil.item_positions[item]
                seg = Segment.MAP_SEGMENT[blocker_pos]
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blockers, self.collected_keys
                )


def search_keys_in_seg_and_children_until_blocked(seg, reachable_keys, blockers, collected_keys):
    for item in seg.ordered_items:
        stopped = False
        if 1 <= item <= 26:  # key
            if collected_keys[item]:
                pass
            else:
                reachable_keys[item] = True
                stopped = True
        elif -26 <= item <= -1:
            if collected_keys[-item]:
                pass
            else:
                # blocked by the door
                stopped = True
        
        # return if stopped
        if stopped:
            blockers[item] = True
            return

    for s in seg.children:
        search_keys_in_seg_and_children_until_blocked(s, reachable_keys, blockers, collected_keys)


if __name__ == '__main__':
    trace_list = []
    start_trace = SearchTrace(True)

    def dfs(search_trace):
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        if np.sum(search_trace.reachable_keys) == 0:
            if min_step > search_trace.step:
                SearchTrace.set_min_step(search_trace.step)
                print(search_trace.step)
                trace_list.append(search_trace)
            return

        for k in range(1,27):
            if not search_trace.reachable_keys[k]:
                continue
            s = search_trace.copy()
            info = s.get_key(k)
            if info != 'abort':
                dfs(s)

    # dfs(start_trace)

    def test():
        for i in [1, 4, 5, 9, 8, 10, 17, 16, 22, 23, 7, 24, 26, 11, 12, 13]:
            start_trace.get_key(i)
            print('blocked', [door for door, _ in start_trace.blockers])
            print('reachable_keys', start_trace.reachable_keys)


    def _bfs(search_trace, task_list):
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        if np.sum(search_trace.reachable_keys) == 0:
            if min_step > search_trace.step:
                with open('day18-result.txt', 'a') as f:
                    f.write('%d %s\n'%(search_trace.step, search_trace.trace.__repr__()))
                SearchTrace.set_min_step(search_trace.step)
                print('min step', search_trace.step)
                trace_list.append(search_trace)

            return

        for k in range(1,27):
            if not search_trace.reachable_keys[k]:
                continue
            s = search_trace.copy()
            info = s.get_key(k)
            if info != 'abort':
                heapq.heappush(task_list, s.pack())


    def bfs_with_heap(start_trace):
        start_trace.pack()
        task_list = [start_trace]

        while task_list:
            s = heapq.heappop(task_list).unpack()
            _bfs(s, task_list)
