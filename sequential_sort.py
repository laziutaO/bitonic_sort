import random
import math

def is_power_of_2_log(n):
    if n <= 0:
        return False
    log2_n = math.log2(n)
    return log2_n.is_integer()

def bitonic_sort(arr, start, sub_arr_len, asc, comparator):
    if not is_power_of_2_log(sub_arr_len):
        raise ValueError("Length of the array must be a power of 2")
    if sub_arr_len > 1:
        sub_arr_len = sub_arr_len // 2
        bitonic_sort(arr, start, sub_arr_len, True, comparator)
        bitonic_sort(arr, start + sub_arr_len, sub_arr_len, False, comparator)
        merge_subarray(arr, start, sub_arr_len * 2, asc, comparator)

def swap_elements(arr, indx1, indx2, asc, comparator):
    comparison_result = comparator(arr[indx1], arr[indx2])
    if (asc and comparison_result > 0) or (not asc and comparison_result < 0):
        arr[indx1], arr[indx2] = arr[indx2], arr[indx1]

def merge_subarray(arr, start, sub_len, asc, comparator):
    if sub_len > 1:
        sub_len = sub_len // 2
        for i in range(start, start + sub_len):
            swap_elements(arr, i, i + sub_len, asc, comparator)
        merge_subarray(arr, start, sub_len, asc, comparator)
        merge_subarray(arr, start + sub_len, sub_len, asc, comparator)

def is_sorted(arr, asc=True, comparator=None):
    if comparator is None:
        comparator = lambda a, b: (a > b) - (a < b)
    
    for i in range(len(arr) - 1):
        if (asc and comparator(arr[i], arr[i + 1]) > 0) or (not asc and comparator(arr[i], arr[i + 1]) < 0):
            return False
    return True


