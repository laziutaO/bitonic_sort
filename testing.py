import random
import time
from sequential_sort import bitonic_sort, is_sorted
from parallel_sort import parallel_bitonic_sort, is_sorted_parallel

class CustomObject:
    def __init__(self, field):
        self.field = field

def module_object_comparator(obj1, obj2):
    return (abs(obj1.field) > abs(obj2.field)) - (abs(obj1.field) < abs(obj2.field))

def number_comparator(a, b):
    return (a > b) - (a < b)

def run_sorts(length, workers, asc):
    input_array = [random.randint(0, 1000000) for _ in range(length)]
    input_array_seq = input_array.copy()
    input_array_par = input_array.copy()

    print(f"Size of array: {length}")

    # Sequential Bitonic Sort
    start_time = time.time()
    bitonic_sort(input_array_seq, 0, length, asc, number_comparator)
    end_time = time.time()
    seq_time_taken = (end_time - start_time)
        
    if is_sorted(input_array_seq, asc=asc, comparator = number_comparator):
        print("Sequential sort: Sorted correctly")
    else:
        print("Sequential sort: Sorted incorrectly")
    
    print("Time taken to sort the array sequentially: {:.6f} seconds".format(seq_time_taken))

    # Parallel Bitonic Sort
    start_time = time.time()
    parallel_bitonic_sort(input_array_par, length, workers, asc, number_comparator)
    end_time = time.time()
    par_time_taken = (end_time - start_time)
    
    if is_sorted_parallel(input_array_par, asc=asc, comparator = number_comparator):
        print("Parallel sort: Sorted correctly")
    else:
        print("Parallel sort: Sorted incorrectly")
    
    print("Time taken to sort the array in parallel: {:.6f} seconds".format(par_time_taken))

    speedup = seq_time_taken / par_time_taken
    print("Speedup: {:.2f}".format(speedup))
    print("="*40)


def run_parallel(lengths, workers, asc):
    for length in lengths:
        arr_objects = [random.uniform(-5000.0, 10000.0) for _ in range(length)]
        print(f"Size of array: {length}")
        start_time = time.time()
        parallel_bitonic_sort(arr_objects, length, workers, asc, number_comparator)
        end_time = time.time()
        if is_sorted_parallel(arr_objects, asc=asc, comparator = number_comparator):
            print("Sorted correctly")
        else:
            print("Sorted incorrectly")
        time_taken = (end_time - start_time) 
        print("Time taken to sort the array: {:.6f} seconds".format(time_taken))
        print("="*40)

def run_sequential(lengths, asc):
    for length in lengths:
        arr_objects = [CustomObject(random.randint(-5000, 10000)) for _ in range(length)]
        print(f"Size of array: {length}")
        start_time = time.time()
        bitonic_sort(arr_objects, 0, length, asc, module_object_comparator)
        end_time = time.time()
        if is_sorted(arr_objects, asc=asc, comparator = module_object_comparator):
            print("Sorted correctly")
        else:
            print("Sorted incorrectly")
        time_taken = (end_time - start_time) 
        print("Time taken to sort the array1: {:.6f} seconds".format(time_taken))
        print("="*40)

if __name__ == "__main__":
    lengths = [2048, 32768, 131072, 262144, 524288, 1048576]
    length = lengths[3]
    asc = True
    workers = 8

    run_sorts(length, asc, workers)
    run_sequential(lengths, asc)
    run_parallel(lengths, workers, asc)
