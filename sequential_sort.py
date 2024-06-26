import time
import random
import math

def swap_elements(arr, indx1, indx2, asc):
    if (asc and arr[indx1] > arr[indx2]) or (not asc and arr[indx1] < arr[indx2]):
        arr[indx1], arr[indx2] = arr[indx2], arr[indx1]

def is_power_of_2_log(n):
    if n <= 0:
        return False
    log2_n = math.log2(n)
    return log2_n.is_integer()

def bitonic_sort(arr, length, asc):
    if not is_power_of_2_log(length):
        raise ValueError("Length of the array must be a power of 2")
    size = 2
    while size <= length:
        for start in range(0, length, size):
            half_size = size // 2
            bitonic_merge(arr, start, half_size, True)
            bitonic_merge(arr, start + half_size, half_size, False)
            bitonic_merge(arr, start, size, asc)
        size *= 2

def bitonic_merge(arr, start, sub_len, asc):
    k = sub_len // 2
    while k > 0:
        for i in range(start, start + sub_len - k):
            swap_elements(arr, i, i + k, asc)
        k //= 2

def is_sorted(arr, asc=True):
    if asc:
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                return False
    else:
        for i in range(len(arr) - 1):
            if arr[i] < arr[i + 1]:
                return False
    return True




