import maputil18 as maputil
import numpy as np
from pylab import imshow, show, figure, pause
import heapq
Segment = maputil.Segment


class SearchTrace:
    min_step = 6060  # this number is obtained from test2()
    @classmethod
    def get_min_step(cls):
        return cls.min_step

    @classmethod
    def set_min_step(cls, value):
        if cls.min_step > value:
            cls.min_step = value

    def __init__(self, to_init_search=False, quadrant=None):
        if quadrant is None:
            self.reachable_keys = np.zeros((1,26+1), np.bool)
            self.blockers = np.zeros((1,26*2+1), np.bool)
            self.head = [(40,40)]
        else:
            self.reachable_keys = np.zeros((4,26+1), np.bool)
            self.blockers = np.zeros((4,26*2+1), np.bool)
            self.head = [(39,41), (39,39), (41,39), (41,41)]

        self.collected_keys = np.zeros(26+1, np.bool)
        self.step = np.uint32(0)
        self.trace = []

        if to_init_search:
            self._initial_search(quadrant)


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
        ret.head = self.head.copy()
        ret.trace = self.trace.copy()
        return ret

    def pack(self):
        self.reachable_keys = np.packbits(self.reachable_keys, axis=-1)
        self.blockers = np.packbits(self.blockers, axis=-1)
        self.collected_keys = np.packbits(self.collected_keys)
        return self

    def unpack(self):
        self.reachable_keys = np.unpackbits(self.reachable_keys, axis=-1)[:,:27]
        self.blockers = np.unpackbits(self.blockers, axis=-1)[:,:26*2+1]
        self.collected_keys = np.unpackbits(self.collected_keys)[:27]
        return self

    def _initial_search(self, quadrant):
        for i in range(4):
            for seg in maputil.quadrants[i]:
                if quadrant is None:
                    search_keys_in_seg_and_children_until_blocked(
                            seg, self.reachable_keys[0], self.blockers[0], self.collected_keys)
                else:
                    search_keys_in_seg_and_children_until_blocked(
                            seg, self.reachable_keys[i], self.blockers[i], self.collected_keys)

    def get_key(self, key):
        key_pos = maputil.item_positions[key]

        if len(self.head) == 1:
            i_robot = 0
        else:
            i_robot = Segment.MAP_SEGMENT[key_pos].quadrant

        assert self.reachable_keys[i_robot, key] == True

        # count the step to move to where the key is
        n_steps = maputil.move(self.head[i_robot], key_pos)
        self.step += n_steps
        self.head[i_robot] = key_pos

        self.reachable_keys[i_robot, key] = False
        self.collected_keys[key] = True
        self.trace = [self.trace, np.uint8(key)]
        obtained_key = key

        if self.step > self.get_min_step():
            return False

        # Check the removed blockers
        for i_robot in range(len(self.head)):
            for item in range(-26,27):
                if not self.blockers[i_robot, item] or item == 0:
                    continue

                if abs(item) == obtained_key:  # this checks for both key and door
                    # Remove the blocker from the list
                    self.blockers[i_robot, item] = False
                    # Recursively search
                    blocker_pos = maputil.item_positions[item]
                    seg = Segment.MAP_SEGMENT[blocker_pos]
                    search_keys_in_seg_and_children_until_blocked(
                        seg, self.reachable_keys[i_robot], self.blockers[i_robot], self.collected_keys
                    )

        return True


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
    # start_trace = SearchTrace(True)

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
            if not search_trace.reachable_keys[0,k]:
                continue
            s = search_trace.copy()
            info = s.get_key(k)
            if info != False:
                dfs(s)

    # dfs(start_trace)

    def test():
        start_trace = SearchTrace(True)
        for i in [1, 4, 5, 9, 8, 10, 17, 16, 22, 23, 7, 24, 26, 11, 12, 13]:
            start_trace.get_key(i)
            print('blocked', [door for door, _ in start_trace.blockers])
            print('reachable_keys', start_trace.reachable_keys)

    def test2():
        start_trace = SearchTrace(True)
        n_keys = 0
        while n_keys != 26:
            for i in range(1,27):
                if start_trace.reachable_keys[0,i]:
                    start_trace.get_key(i)
                    n_keys += 1
                    break

        print(start_trace.step)


    max_num_of_keys_collected = 0
    def _bfs(search_trace, task_list):
        global max_num_of_keys_collected
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        n_collected_keys = np.sum(search_trace.collected_keys)
        if n_collected_keys == 26:
            if min_step > search_trace.step:
                print('min step', search_trace.step)
                with open('day18-result.txt', 'a') as f:
                    curr_trace = search_trace.trace
                    to_write = []
                    while curr_trace:
                        to_write.append(curr_trace[-1])
                        curr_trace = curr_trace[0]
                    to_write = to_write[::-1]
                    f.write('%d %s\n'%(search_trace.step, to_write.__repr__()))
                SearchTrace.set_min_step(search_trace.step)
                trace_list.append(search_trace)
            return
        
        if max_num_of_keys_collected < n_collected_keys:
            max_num_of_keys_collected = n_collected_keys
            print('keys:', n_collected_keys, ' steps:', search_trace.step, ' task:', len(task_list))

        touched = False
        reachable_keys = search_trace.reachable_keys.sum(axis=0)
        group_ej = False
        group_dqz = False
        group_mvw = False
        for k in range(1,27):
            if not reachable_keys[k]:
                continue
            touched = True
            s = search_trace.copy()
            if   k == 20:  # tu
                if not s.get_key(20): continue  # t
                if not s.get_key(21): continue  # u
            elif k == 19:  # sbor
                if not s.get_key(19): continue  # s
                if not s.get_key( 2): continue  # b
                if not s.get_key(15): continue  # o
                if not s.get_key(18): continue  # r
            elif k == 11:  # kgx
                if not s.get_key(11): continue  # k
                if not s.get_key( 7): continue  # g
                if not s.get_key(24): continue  # x
            elif k in [5,10]:  # ej
                if group_ej:
                    continue
                group_ej = True
                if not s.get_key( 5): continue  # e
                if not s.get_key(10): continue  # j
            elif k in [4,17,26]:  # dqz
                if group_dqz:
                    continue
                group_dqz = True
                if not s.get_key( 4): continue  # d
                if not s.get_key(17): continue  # q
                if not s.get_key(26): continue  # z
            elif k in [13,22,23]:  # mvw
                if group_mvw:
                    continue
                group_mvw = True
                if not s.get_key(23): continue  # w
                if not s.get_key(13): continue  # m
                if not s.get_key(22): continue  # v
            else:
                if not s.get_key(k):
                    continue
            heapq.heappush(task_list, s.pack())
        assert touched

    def bfs_with_heap(start_trace):
        start_trace.pack()
        task_list = [start_trace]

        while task_list:
            s = heapq.heappop(task_list).unpack()
            _bfs(s, task_list)

    # Part 1
    # bfs_with_heap(SearchTrace(True))

    # Part 2
    bfs_with_heap(SearchTrace(True, quadrant='all'))
