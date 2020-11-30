from util_binsearch import binarySearch


def swap(a, b):
    return b, a


def merge(vector, start_sub1, end_sub1, start_sub2, end_sub2, start_merged=0, merged=None):
    n1, n2 = end_sub1 - start_sub1, end_sub2 - start_sub2
    if n1 < n2:
        p, r = swap(start_sub1, start_sub2), swap(end_sub1, end_sub2)
    else:
        p, r = (start_sub1, start_sub2), (end_sub1, end_sub2)
    start_sub1, start_sub2, end_sub1, end_sub2 = p[0], p[1], r[0], r[1]     # make sub1 the longest one
    if merged is None:
        merged = {i: vector[i] for i in range(start_merged, start_merged + n1 + n2)}
    if not (max(n1, n2) == 0):
        mid_sub1 = (start_sub1 + end_sub1) // 2
        split_sub2 = binarySearch(vector, start_sub2, end_sub2, vector[mid_sub1])
        split_merged = start_merged + (split_sub2 - start_sub2) + (mid_sub1 - start_sub1)
        merged[split_merged] = vector[mid_sub1]
        merge(vector, start_sub1, mid_sub1, start_sub2, split_sub2, start_merged, merged)
        merge(vector, mid_sub1 + 1, end_sub1, split_sub2, end_sub2, split_merged + 1, merged)
    if len(merged) == (n1 + n2):
        vector[start_merged:(start_merged + n1 + n2)] = [merged[i] for i in sorted(merged.keys())]


def mergeSort(vector, start=0, end=None):
    if end is None:
        end = len(vector)
    if (start + 1) < end:
        mid = (start + end) // 2
        mergeSort(vector, start, mid)
        mergeSort(vector, mid, end)
        merge(vector, start, mid, mid, end, start)


if __name__ == "__main__":
    # t1, t2 = [3, 4, 6, 8, 9], [1, 5, 7, 10]
    p = 0
    pad, t1, t2 = [None] * p, [-1, 5, 8], [4, 7]
    t = pad + t1 + t2
    print(t)
    merge(t, p, p + len(t1), p + len(t1), p + len(t1) + len(t2), start_merged=p)
    print(t)
    print("----------------------------------------------")
    u = [10, 1, 5, -1, 7, 4, 0, 3, 2, 0, 15, 8]
    print(u)
    mergeSort(u)
    print(u)

