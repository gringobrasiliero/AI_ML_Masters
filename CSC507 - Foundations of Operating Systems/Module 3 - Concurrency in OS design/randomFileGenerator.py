#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import threading
import os
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import queue # imported for using queue.Empty exception

txt_file_name = "file2.txt"

def make_random_nums(line_count):
    random_nums=""
    for i in  range(line_count):
        random_nums += str(random.randint(0,32767)) + "\n"
    return random_nums

def write_to_open_file(f,num_count):
    nums = make_random_nums(num_count)
    f.write(nums)

def multithreading(thread_count, num_count):
    threads = []
    with open(txt_file_name, 'w') as f:
        for i in range(thread_count):
            threads.append(threading.Thread(target=write_to_open_file, args=(f,num_count), name='thread-'+str(i)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

def generate_nums():
    nums = ""
    for i in  range(100000):
        nums += str(random.randint(0,32767)) + "\n"
    return nums

def producer(queue):
    for i in range(10):
        value=generate_nums()
        queue.put(value)
    queue.put(None)

def consumer(queue):
    with open(txt_file_name, 'w') as f:
        while True:
            item = queue.get()
            # check for stop
            if item is None:
                break
            f.write(item)
    
def multi_processing():
    queue = Queue()
    # start the consumer
    consumer_process = Process(target=consumer, args=(queue,))
    consumer_process.start()
    # start the producer
    producer_process = Process(target=producer, args=(queue,))
    producer_process.start()
    # wait for all processes to finish
    producer_process.join()
    consumer_process.join()

def line_count_test(expected_line_count):
    with open(txt_file_name, 'r') as fp:
        x = len(fp.readlines())
        print('Total lines:', x)
    if x == expected_line_count:
        print("Line Count Test: PASS")
    else:
        print("Line Count Test: FAIL")
        print("\tExpected " + str(expected_line_count))
        print("\tCounted " + str(x))

def main():
    expected_line_count = 1000000

    start = time.time() # Start time of Multithreading with 2 threads
    multithreading(2,500000)
    end = time.time() # End time of Multithreading with 2 threads
    ms = (end-start) * 10**3
    print("Multithreading with 2 Threads Time: " + str(ms) + " ms")
    line_count_test(expected_line_count)
    os.remove(txt_file_name)

    start = time.time() # Start time of Multithreading with 5 threads
    multithreading(5,200000)
    end = time.time() # End time of Multithreading with 5 threads
    ms = (end-start) * 10**3
    print("Multithreading with 5 threads Time: " + str(ms) + " ms")
    line_count_test(expected_line_count)
    os.remove(txt_file_name)

    start = time.time() # Start time of Multithreading with 10 threads
    multithreading(10,100000)
    end = time.time() # End time of Multithreading with 10 threads
    ms = (end-start) * 10**3
    print("Multithreading with 10 threads Time: " + str(ms) + " ms")
    line_count_test(expected_line_count)
    os.remove(txt_file_name)

    start = time.time() # Start time of Multiprocessing
    multi_processing()
    end = time.time() # End Time of Multiprocessing
    ms = (end-start) * 10**3
    print("Multi-Processing Time: " + str(ms) + " ms")
    line_count_test(expected_line_count)

    pass





if __name__ == '__main__' : main()

