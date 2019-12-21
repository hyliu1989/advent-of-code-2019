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
            for seg in quad:
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blocked_lock_and_segments,
                    self.collected_keys)

    def get_key(self, key):
        assert key in self.reachable_keys

        # count the step to move to where the key is
        key_pos = maputil.item_positions[key]
        key_seg = maputil.segment_map[key_pos]
        try:
            curr_step = 0
            if self.head == (40,40):
                for item, nth_tile in key_seg.ordered_items:
                    if item == key:
                        curr_step += nth_tile
                        break

                curr_step += count_steps_until_entering_the_ancestor(key_seg, collected_keys=self.collected_keys)
                curr_step += 2
            else:
                head_seg = maputil.segment_map[self.head]
                p1, p2 = maputil.find_common_parent(head_seg, key_seg)
                collected = self.collected_keys
                if p2 is not None:
                    assert p1 in range(4)
                    assert p2 in range(4)
                    # head and the key are in different quadrants
                    curr_step += head_seg.segment[self.head]-1
                    curr_step += count_steps_until_entering_the_ancestor(head_seg, collected_keys=collected)
                    if (p1,p2) in [(0,2), (2,0), (1,3), (3,1)]:
                        curr_step += 5
                    else:
                        curr_step += 3
                    curr_step += count_steps_until_entering_the_ancestor(key_seg, collected_keys=collected)
                    curr_step += key_seg.segment[key_pos]
                else:
                    # head and the key are in the same quadrant
                    if p1 is key_seg:
                        curr_step += head_seg.segment[self.head] - 1
                        curr_step += count_steps_until_entering_the_ancestor(
                            head_seg, ancestor_seg=key_seg, collected_keys=collected)
                        curr_step += key_seg.length - key_seg.segment[key_pos] + 1
                    elif p1 is head_seg:
                        curr_step += head_seg.length - head_seg.segment[self.head]
                        curr_step += count_steps_until_entering_the_ancestor(
                            key_seg, ancestor_seg=head_seg, collected_keys=collected)
                        curr_step += key_seg.segment[key_pos]
                    else:
                        # p1 is some segment in between or the head of the quadrant
                        curr_step += head_seg.segment[self.head] - 1
                        curr_step += count_steps_until_entering_the_ancestor(
                            head_seg, ancestor_seg=p1, collected_keys=collected)
                        curr_step += 1
                        curr_step += count_steps_until_entering_the_ancestor(
                            key_seg, ancestor_seg=p1, collected_keys=collected)
                        curr_step += key_seg.segment[key_pos]
        except RuntimeError as e:
            print(e)
            return 'abort'
        self.step += curr_step
        self.head = key_pos

        self.reachable_keys.remove(key)
        self.collected_keys.add(key)
        self.trace.append(key)

        if self.step > self.get_min_step():
            return 'abort'

        original = self.blocked_lock_and_segments.copy()
        for locked_door, seg in original:
            if locked_door == -key:
                # the locked door is unlocked!
                self.blocked_lock_and_segments.remove((locked_door, seg))
                search_keys_in_seg_and_children_until_blocked(
                    seg, self.reachable_keys, self.blocked_lock_and_segments,
                    self.collected_keys)


def count_steps_until_entering_the_ancestor(current_seg, *, ancestor_seg=None,
                                            collected_keys=set()):
    step = 0
    p = current_seg.parent
    while True:
        if p == ancestor_seg or p in range(4):
            break
        for item, _ in p.ordered_items:
            if 1 <= item <= 26 and item not in collected_keys:
                raise RuntimeError("an uncollected key '%c' is in the way of moving!" % chr(item-1+ord('a')))
        step += p.length
        p = p.parent
    return step


def search_keys_in_seg_and_children_until_blocked(seg, keys, blocked_lock_and_segments, 
                                                  collected_keys):
    for item, _ in seg.ordered_items:
        if 1 <= item <= 26:
            keys.add(item)
        elif -26 <= item <= -1:
            if -item not in collected_keys:
                # blocked by the door
                blocked_lock_and_segments.append((item, seg))
                return
    for s in seg.children:
        search_keys_in_seg_and_children_until_blocked(s, keys, blocked_lock_and_segments,
                                                      collected_keys)


if __name__ == '__main__':
    trace_list = []
    start_trace = SearchTrace(True)

    def dfs(search_trace):
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

    dfs(start_trace)
