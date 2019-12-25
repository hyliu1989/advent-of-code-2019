import maputil18 as maputil
import numpy as np
from pylab import imshow, show, figure, pause
import numba

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
        self.blockers =  np.zeros(26*2+1, np.int8)
        self.collected_keys = np.zeros(26+1, np.bool)
        self.step = 0
        self.head = (40,40)
        self.trace = []

        if to_init_search:
            self._initial_search()

    def copy(self):
        ret = SearchTrace()
        ret.reachable_keys = self.reachable_keys.copy()
        ret.blockers = self.blockers.copy()
        ret.collected_keys = self.collected_keys.copy()
        ret.step = self.step
        ret.head = self.head
        ret.trace = self.trace.copy()
        return ret

    def _initial_search(self):
        for quad in maputil.quadrants:
        # for quad in [maputil.quadrants[1][1:2]]:
            for seg in quad:
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blockers, self.collected_keys
                )

    def get_key(self, key):
        assert self.reachable_keys[key] == True

        # count the step to move to where the key is
        key_pos = maputil.item_positions[key]
        n_steps = maputil.move(self.head, key_pos)

        self.step += n_steps
        self.head = key_pos

        self.reachable_keys[key] = False
        self.collected_keys[key] = True
        self.trace.append(key)
        obtained_key = key

        if self.step > self.get_min_step():
            return 'abort'

        # Check the removed blockers
        idx_blocker = 0
        for idx_blocker in range(self.blockers.size):
            # get the iterate of the blocker
            item = self.blockers[idx_blocker]
            if item == 0:
                break

            blocker_pos = maputil.item_positions[item]
            seg = maputil.segment_map[blocker_pos]
            if abs(item) == obtained_key:  # this checks for both key and door. If True, unlock the blocker.
                # Remove the blocker from the list
                self.blockers[idx_blocker:-1] = self.blockers[idx_blocker+1:]
                # Recursively search
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blockers,
                    self.collected_keys)


@numba.jit(nopython=True, nogil=True)
def search_keys_in_seg_and_children_until_blocked(
    seg, reachable_keys, blockers, collected_keys,
    db_ordered_item=maputil.segment_db['ordered_items'],
    db_children=maputil.segment_db['children'],
):
    # search both the key and the door inside seg
    for i in range(db_ordered_item.shape[1]):
        # get the iterate of the ordered_item
        item = db_ordered_item[seg,i]
        if item == 0:
            break

        # check the key
        stopped = False
        if 1 <= item <= 26:  # key
            if collected_keys[item]:
                pass
            else:
                reachable_keys[item] = True
                stopped = True
        # check the door
        elif -26 <= item <= -1:
            if collected_keys[-item]:
                pass
            else:
                # blocked by the door
                stopped = True
        # return if stopped
        if stopped:
            for idx_blocker in range(blockers.size):
                if blockers[idx_blocker] == 0:
                    break
            blockers[idx_blocker] = item
            return 0

    # if not stopped, continue searching seg's children
    for i in range(db_children.shape[1]):
        # get the iterate of children
        s = db_children[seg,i]
        if s == -1:
            break

        # recursively search
        search_keys_in_seg_and_children_until_blocked(s, reachable_keys, blockers, collected_keys)

    return 0

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
            print('blocked', [blocker for blocker in start_trace.blockers if blocker != 0])
            print('reachable_keys', start_trace.reachable_keys)

    task_list = []

    def _bfs(search_trace):
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        for k in range(1,27):
            if not search_trace.reachable_keys[k]:
                continue
            s = search_trace.copy()
            info = s.get_key(k)
            if info != 'abort':
                task_list.append(s)

    def bfs_and_dfs(start_trace):
        global task_list
        n_collected_keys = 0

        task_list.append(start_trace)
        while len(task_list[:1]) != 0:
            n_keys_new = np.sum(task_list[0].collected_keys)
            if n_collected_keys != n_keys_new:
                # sort
                print('task_list[0:2] steps (before sort)', task_list[0].step, task_list[1].step)
                task_list = sorted(task_list, key=lambda x: x.step)
                print('task_list[0:2] steps (after sort) ', task_list[0].step, task_list[1].step)
                print('len(list)', len(task_list))
                print('='*40)
            n_collected_keys = n_keys_new

            if n_keys_new == 7:
                n_collected_keys = n_keys_new
                break

            s = task_list[0]
            task_list = task_list[1:]
            _bfs(s)

        for s in task_list:
            dfs(s)

# TODO: The value does not match the previous run!!!
