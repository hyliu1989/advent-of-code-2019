import maputil18 as maputil
import numpy as np
from pylab import imshow, show, figure, pause

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
        self.reachable_keys = set()
        self.blocked_lock_and_segments = []
        self.collected_keys = set()
        self.step = 0
        self.head = (40,40)
        self.trace = []

        if to_init_search:
            self._initial_search()

    def copy(self):
        ret = SearchTrace()
        ret.reachable_keys = self.reachable_keys.copy()
        ret.blocked_lock_and_segments = self.blocked_lock_and_segments.copy()
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
                    seg, self.reachable_keys, self.blocked_lock_and_segments,
                    self.collected_keys)

    def get_key(self, key):
        assert key in self.reachable_keys

        # count the step to move to where the key is
        key_pos = maputil.item_positions[key]
        n_steps = maputil.move(self.head, key_pos)

        self.step += n_steps
        self.head = key_pos

        self.reachable_keys.remove(key)
        self.collected_keys.add(key)
        self.trace.append(key)

        if self.step > self.get_min_step():
            return 'abort'

        original = self.blocked_lock_and_segments.copy()
        for item, seg in original:
            if abs(item) == key:  # check for both key and door
                # the locked door is unlocked!
                self.blocked_lock_and_segments.remove((item, seg))
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blocked_lock_and_segments,
                    self.collected_keys)


def search_keys_in_seg_and_children_until_blocked(seg, reachable_keys, blocked_lock_and_segments,
                                                  collected_keys):
    for item, _ in seg.ordered_items:
        stopped = False
        if 1 <= item <= 26:  # key
            if item in collected_keys:
                pass
            else:
                reachable_keys.add(item)
                stopped = True
        elif -26 <= item <= -1:
            if -item in collected_keys:
                pass
            else:
                # blocked by the door
                stopped = True
        if stopped:
            blocked_lock_and_segments.append((item, seg))
            return

    for s in seg.children:
        search_keys_in_seg_and_children_until_blocked(s, reachable_keys, blocked_lock_and_segments,
                                                      collected_keys)


if __name__ == '__main__':
    trace_list = []
    start_trace = SearchTrace(True)

    def dfs(search_trace):
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        if len(search_trace.reachable_keys) == 0:
            if min_step > search_trace.step:
                SearchTrace.set_min_step(search_trace.step)
                print(search_trace.step)
                trace_list.append(search_trace)
            return

        for k in search_trace.reachable_keys:
            s = search_trace.copy()
            info = s.get_key(k)
            if info != 'abort':
                dfs(s)

    # dfs(start_trace)

    def test():
        for i in [1, 4, 5, 9, 8, 10, 17, 16, 22, 23, 7, 24, 26, 11, 12, 13]:
            start_trace.get_key(i)
            print('blocked', [door for door, _ in start_trace.blocked_lock_and_segments])
            print('reachable_keys', start_trace.reachable_keys)


    def _bfs(search_trace, task_list):
        # record only the trace that requires the minimal step
        min_step = SearchTrace.get_min_step()
        if len(search_trace.reachable_keys) == 0:
            if min_step > search_trace.step:
                SearchTrace.set_min_step(search_trace.step)
                print('min step', search_trace.step)
                trace_list.append(search_trace)
            return

        for k in search_trace.reachable_keys:
            s = search_trace.copy()
            info = s.get_key(k)
            if info != 'abort':
                task_list.append(s)


    def bfs_with_batch(start_trace):
        curr_key_num = 0
        curr_task_list = [start_trace]
        task_lists_later = {}
        threshold = 100000

        while True:
            task_list_more_key = []
            while curr_task_list:
                s = curr_task_list[0]
                curr_task_list = curr_task_list[1:]
                _bfs(s, task_list_more_key)

            if len(task_list_more_key) > threshold:
                saved = task_lists_later.get(curr_key_num+1)
                if saved:
                    task_list_more_key += saved
                task_list_more_key = sorted(task_list_more_key, key=lambda x: x.step)
                task_lists_later[curr_key_num+1] = task_list_more_key[threshold:]
                task_list_more_key = task_list_more_key[:threshold]
            else:
                task_list_more_key = sorted(task_list_more_key, key=lambda x: x.step)
            
            curr_task_list = task_list_more_key
            curr_key_num += 1

            if not curr_task_list:
                while True:
                    curr_key_num -= 1
                    task_list_temp = task_lists_later.get(curr_key_num)
                    if task_list_temp:
                        curr_task_list = task_list_temp[:threshold]
                        task_list_temp = task_list_temp[threshold:]
                        task_lists_later[curr_key_num] = task_list_temp
                        break
                    if curr_key_num == 0:
                        return
