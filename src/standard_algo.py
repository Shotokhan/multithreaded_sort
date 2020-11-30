def merge(vector, start, mid, end):
    '''
    Preconditions: start <= mid <= end, vector[p:q] and vector[q:r] ordered
    :param vector: Array containing ordered subarray to merge, assumed adjacent
    :param start: Starting index of the first subarray
    :param mid: Starting index of the second subarray
    :param end: Index of the element consecutive to the last element of the second subarray
    Postcondition: vector[p:r] is an ordered subarray with elements in vector[p:q] and vector[q:r]
    '''
    i, j = 0, 0
    left, right = vector[start:mid] + [float('inf')], vector[mid:end] + [float('inf')]
    for k in range(start, end):
        if left[i] < right[j]:
            vector[k] = left[i]
            i += 1
        else:
            vector[k] = right[j]
            j += 1


def mergeSort(A, start=0, end=None):
    if end is None:
        end = len(A)
    if (start + 1) < end:
        mid = (start + end) // 2
        mergeSort(A, start, mid)
        mergeSort(A, mid, end)  # Python is inclusive at left and not at right
        merge(A, start, mid, end)


if __name__ == "__main__":
    t1, t2 = [3, 4, 6, 8, 9], [1, 5, 7, 10]
    t = t1 + t2
    print(t)
    merge(t, 0, len(t1), len(t1) + len(t2))
    print(t)
    print("----------------------------------------------")
    u = [10, 1, 5, -1, 7, 4, 0, 3, 2, 0, 15, 8]
    print(u)
    mergeSort(u)
    print(u)
