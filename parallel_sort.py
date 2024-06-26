import time
import random
import multiprocessing
import math

def swap_elements(arr, indx1, indx2, asc):
    if (asc and arr[indx1] > arr[indx2]) or (not asc and arr[indx1] < arr[indx2]):
        arr[indx1], arr[indx2] = arr[indx2], arr[indx1]

def bitonic_merge(arr, start, sub_len, asc):
    k = sub_len // 2
    while k > 0:
        for i in range(start, start + sub_len - k):
            if i + k < len(arr):  
                swap_elements(arr, i, i + k, asc)
        k //= 2
 

def batch_split_swap(shared_arr, start_indices, size, asc):
    half_size = size // 2
    for start in start_indices:
        bitonic_merge(shared_arr, start, half_size, True)
        bitonic_merge(shared_arr, start + half_size, half_size, False)

def is_power_of_2_log(n):
    if n <= 0:
        return False
    log2_n = math.log2(n)
    return log2_n.is_integer()

def parallel_bitonic_sort(arr, length, workers, asc):
    if not is_power_of_2_log(length):
        raise ValueError("Length of the array must be a power of 2")
    size = 2
    max_worker = workers

    pool = multiprocessing.Pool(processes=max_worker)
    while size <= length:
        batch_size = length // max_worker
        batches = [range(i, min(i + batch_size, length), size) for i in range(0, length, batch_size)]
        result = [pool.apply_async(batch_split_swap, args= (arr, list(batch), size, asc)) for batch in batches]

        for start in range(0, length, size):
            bitonic_merge(arr, start, size, asc)

        size *= 2

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



