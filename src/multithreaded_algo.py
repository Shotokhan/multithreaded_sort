from threading import Thread
from util_binsearch import binarySearch
from multiprocessing import cpu_count
from math import log2
import standard_algo
import binmerge


n_threads = 2**int(log2(cpu_count()))   # pointless to have more running threads than available cores


def mergeSort(vector, start=0, end=None):
    if end is None:
        end = len(vector)
    merge_sort = MergeSort(vector, start, end)
    merge_sort.start()
    merge_sort.join()


class MergeSort(Thread):
    def __init__(self, shared_vect, start=0, end=None, depth=0):
        super().__init__()
        self.vector = shared_vect
        self.vect_start = start
        self.vect_end = end if end is not None else len(self.vector)
        self.depth = depth
        # print("Hello I'm a Merge Sort Thread with depth {}".format(self.depth))

    def run(self):
        if (self.vect_start + 1) < self.vect_end:
            vect_mid = (self.vect_start + self.vect_end) // 2
            if (2 ** self.depth) < n_threads:
                merge_sort_left = MergeSort(self.vector, self.vect_start, vect_mid, self.depth + 1)
                merge_sort_left.start()
                merge_sort_right = MergeSort(self.vector, vect_mid, self.vect_end, self.depth + 1)
                merge_sort_right.start()
                merge_sort_left.join()
                merge_sort_right.join()
                merge = Merge(self.vector, self.vect_start, vect_mid, vect_mid, self.vect_end, self.vect_start,
                              depth=self.depth)
                merge.start()
                merge.join()
            else:
                standard_algo.mergeSort(self.vector, self.vect_start, vect_mid)
                standard_algo.mergeSort(self.vector, vect_mid, self.vect_end)
                standard_algo.merge(self.vector, self.vect_start, vect_mid, self.vect_end)


class Merge(Thread):
    # vectors to merge don't need to be adjacent; they still need to be ordered, of course
    def __init__(self, shared_vect, start_sub1, end_sub1, start_sub2, end_sub2, start_merged=0, merged_vect=None,
                 depth=0):
        super().__init__()
        self.vector = shared_vect
        self.start_merged = start_merged  # start of merging point
        # lengths of vectors; recall that in python right bound is not included
        self.n1, self.n2 = end_sub1 - start_sub1, end_sub2 - start_sub2
        if self.n1 < self.n2:  # ensure n1 < n2 for the algorithm
            self.start_sub1, self.end_sub1, self.start_sub2, self.end_sub2 = start_sub2, end_sub2, start_sub1, end_sub1
        else:
            self.start_sub1, self.end_sub1, self.start_sub2, self.end_sub2 = start_sub1, end_sub1, start_sub2, end_sub2
        if merged_vect is None:     # can't do all in place
            self.merged_vect = {i: self.vector[i] for i in range(start_merged, start_merged + self.n1 + self.n2)}
        else:
            self.merged_vect = merged_vect
        self.depth = depth
        # print("Yo I'm a Merge Thread with depth {}".format(self.depth))

    def run(self):
        if not max(self.n1, self.n2) == 0:  # exit if they're both empty
            mid_sub1 = (self.start_sub1 + self.end_sub1) // 2  # split the first vector by half
            # split the second vector by value
            split_sub2 = binarySearch(self.vector, self.start_sub2, self.end_sub2, self.vector[mid_sub1])
            split_merged = self.start_merged + (split_sub2 - self.start_sub2) + (mid_sub1 - self.start_sub1)
            self.merged_vect[split_merged] = self.vector[mid_sub1]
            if (2 ** self.depth) < n_threads:
                merge_left = Merge(self.vector, self.start_sub1, mid_sub1, self.start_sub2, split_sub2,
                                   self.start_merged, self.merged_vect, self.depth + 1)
                merge_left.start()
                merge_right = Merge(self.vector, mid_sub1 + 1, self.end_sub1, split_sub2, self.end_sub2,
                                    split_merged + 1, self.merged_vect, self.depth + 1)
                merge_right.start()
                merge_left.join()
                merge_right.join()
            else:
                binmerge.merge(self.vector, self.start_sub1, mid_sub1, self.start_sub2, split_sub2,
                               self.start_merged, self.merged_vect)
                binmerge.merge(self.vector, mid_sub1 + 1, self.end_sub1, split_sub2, self.end_sub2,
                               split_merged + 1, self.merged_vect)
        if len(self.merged_vect) == (self.n1 + self.n2):
            self.vector[self.start_merged:(self.start_merged + self.n1 + self.n2)] = \
                [self.merged_vect[i] for i in sorted(self.merged_vect.keys())]


if __name__ == "__main__":
    u = [10, 1, 5, -1, 7, 4, 0, 3, 2, 0, 15, 8]
    print(u)
    mergeSort(u)
    print(u)
