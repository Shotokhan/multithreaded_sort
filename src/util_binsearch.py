def binarySearch(A, p, r, x):
    """
    Precondition: A is ordered
    :param A: Ordered array
    :param p: Starting index of the binary search
    :param r: Index of the element that is next to the last element of the binary search
    :param x: Value to be searched
    :return: Index q in the range [p,r] , with q being the largest index such that A[q-1] < x or equal to p
    """
    low, high = p, max(p, r)
    while low < high:
        q = (low + high) // 2
        if x == A[q]:
            return q
        elif x < A[q]:
            high = q
        else:
            low = q + 1
    return high
