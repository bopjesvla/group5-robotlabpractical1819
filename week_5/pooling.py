'''
In this tutorial I will show you the basics of how to do concurrent programming in Python using pool
You do NOT need a Nao for this part
'''

from multiprocessing import Pool
from multiprocessing import freeze_support  # Necessary for Windows.
import numpy as np
from time import time


def count(numbers):
    total = 0
    for i in numbers:
        total += i
        print('total: %d' % total)


def run_sequential(numbers):
    _start = time()
    for i in numbers:
        count(i)
    print('sequential time: %.2f seconds' % (time() - _start))


def parallelize(func, numbers, num_procs):
    pool = Pool(processes=num_procs)
    pool.apply_async(func)
    pool.map(func, numbers)


def run_parallel(func, numbers, num_proc=5):
    _start = time()
    parallelize(func, numbers, num_proc)
    print('parallel time: %.2f seconds' % (time() - _start))


if __name__ == '__main__':
    freeze_support()
    random_numbers = np.random.randint(low=0, high=10, size=(100, 1000))
    run_sequential(numbers=random_numbers)
    run_parallel(func=count, numbers=random_numbers, num_proc=3)
    run_parallel(func=count, numbers=random_numbers, num_proc=6)
