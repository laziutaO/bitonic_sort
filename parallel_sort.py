import multiprocessing
import math

def swap_elements(arr, indx1, indx2, asc, comparator):
    comparison_result = comparator(arr[indx1], arr[indx2])
    if (asc and comparison_result > 0) or (not asc and comparison_result < 0):
        arr[indx1], arr[indx2] = arr[indx2], arr[indx1]

def bitonic_merge(arr, start, sub_len, asc, comparator):
    k = sub_len // 2
    while k > 0:
        for i in range(start, start + sub_len - k):
            if i + k < len(arr):
                swap_elements(arr, i, i + k, asc, comparator)
        k //= 2


def batch_split_swap(shared_arr, start_indices, size, comparator, pool):
    half_size = size // 2
    tasks = []
    for start in start_indices:
        tasks.append(pool.apply_async(bitonic_merge, args=(shared_arr, start, half_size, True, comparator)))
        tasks.append(pool.apply_async(bitonic_merge, args=(shared_arr, start + half_size, half_size, False, comparator)))
    [task.wait() for task in tasks]


def is_power_of_2_log(n):
    if n <= 0:
        return False
    log2_n = math.log2(n)
    return log2_n.is_integer()

def parallel_bitonic_sort(arr, length, workers, asc, comparator):
    if not is_power_of_2_log(length):
        raise ValueError("Length of the array must be a power of 2")
    size = 2
    shared_arr = multiprocessing.Array('i', arr)

    while size <= length:
        batch_size = length // workers
        batches = [range(i, min(i + batch_size, length), size) for i in range(0, length, batch_size)]
        with multiprocessing.Pool(workers) as pool:
            tasks = [
                pool.apply_async(batch_split_swap, (shared_arr, list(batch), size, comparator, pool))
                for batch in batches
            ]
            [task.wait() for task in tasks]

        size *= 2

    arr[:] = list(shared_arr)

def is_sorted_parallel(arr, asc=True, comparator=None):
    if comparator is None:
        comparator = lambda x, y: (x > y) - (x < y)  
    if asc:
        for i in range(len(arr) - 1):
            if comparator(arr[i], arr[i + 1]) > 0:
                return False
    else:
        for i in range(len(arr) - 1):
            if comparator(arr[i], arr[i + 1]) < 0:
                return False
    return True




