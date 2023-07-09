
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import random
import time
import threading
import os
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
#import multiprocessing
import queue # imported for using queue.Empty exception
import shutil


def method_one(arg1, arg2):
    with open("file1.txt", 'r') as read_file:
        with open("new_file1.txt",'w') as write_file:
            line = read_file.readline()
            while line:
                file_one_num = int(line.strip())
                doubled_num = file_one_num * 2
                write_file.write(str(doubled_num) + "\n")
                line = read_file.readline()
    pass

def method_three():
    with open("newfile1.txt",'w') as write_file:
        half_data = pd.read_csv("file1.txt", nrows=500000, header=None)[0].values.tolist()
        for i in range(0,len(half_data)):
            file_one_num = int(half_data[i])
            doubled_num = file_one_num * 2
            write_file.write(str(doubled_num) + "\n")
        
        half_data = pd.read_csv("file1.txt", skiprows=500000, nrows=500000,  header=None)[0].values.tolist()
        for i in range(0,len(half_data)):
            file_one_num = int(half_data[i])
            doubled_num = file_one_num * 2
            write_file.write(str(doubled_num) + "\n")
        pass

def process_slice_of_file(file_name, output_file_name, skip_rows, num_rows ):
    with open(output_file_name,'w') as write_file:
        
        data = pd.read_csv(file_name, skiprows=skip_rows, nrows=num_rows,  header=None)[0].values.tolist()
        for i in range(0,len(data)):
            file_one_num = int(data[i])
            doubled_num = file_one_num * 2
            write_file.write(str(doubled_num) + "\n")
        pass
    
def combine_files(destination_file,num_files):

    for i in range(num_files):
        file = str(i) + ".txt"

        combine_file(file,destination_file)


def combine_file(source_file, destination_file):
    file_source = open(source_file, 'r')
    destination = open(destination_file,'a')
    shutil.copyfileobj(file_source, destination)
    destination.close()
    file_source.close()
    os.remove(source_file)

def generate_queue(queue_len,num_cores):
    queue = Queue()
    for i in range(queue_len):
        queue.put(i)
    for i in range(num_cores):
        queue.put(None)
    return queue


def queue_consumer(queue,file_name, num_rows):
    while True:
        item = queue.get()
        if item is None:
            break
        output_file_name = str(item) + ".txt"
        skip_rows = int(item) * num_rows
        process_slice_of_file(file_name, output_file_name, skip_rows, num_rows)
    pass


def trial_one(num_files,num_cores):
    queue = generate_queue(num_files, num_cores)
    total_row_count = 10000000
    rows_per_file = int(total_row_count / num_files)
    file_name = 'file1.txt'
    destination_file = 'new_file1.txt'
  
    queue_consumer(queue,file_name, rows_per_file)
    combine_files(destination_file, num_files)
    pass


def multi_processing(num_files, num_cores):
    queue = generate_queue(num_files,num_cores)
    total_row_count = 10000000

    rows_per_file = int(total_row_count / num_files)
    file_name = 'file1.txt'
    destination_file = 'new_file1.txt'
    
    processes = []
    for i in range(num_cores):
        process = Process(target=queue_consumer, args=(queue, file_name, rows_per_file,))
        processes.append(process)
        process.start()
        
    for p in processes:
        p.join()
    
    combine_files(destination_file, num_files)
    pass





    
def speed_test(test_name, test_function, args, txt_file_name, num_tests):
    execution_times = []
    for i in range(num_tests):
        start = time.time() # Start time of executing function
        test_function(args[0], args[1])
        end = time.time() # End time of executing function
        ms = (end-start) * 10**3
        execution_times.append(ms)
        os.remove(txt_file_name)
    average_milliseconds = sum(execution_times) / len(execution_times)
    print("Average Execution time of '" + test_name + "' had an Average of " +  str(average_milliseconds) + " ms. with " + str(num_tests) + " trials.")

def main():
    destination_file = 'new_file1.txt'
    num_tests = 3
    print("Number of Cores Available : ", cpu_count())
    
    args = [1, 1] #1 Files, One Core Running
    speed_test("Original Function", method_one, args, destination_file, num_tests)

    args = [2, 1] #2 Files, One Core Running
    speed_test("2 file Split", trial_one, args, destination_file, num_tests)

    args = [5, 1] #5 Files, One Core Running
    speed_test("5 file Split", trial_one, args, destination_file, num_tests)

    args = [10, 1] #10 Files, One Core Running
    speed_test("10 file Split", trial_one, args, destination_file, num_tests)

    args = [20, 1] #20 Files, One Core Running
    speed_test("20 file Split", trial_one, args, destination_file, num_tests)

    print("\n\n")

    args = [2, 2] # 2 Files, 2 Cores Running
    speed_test("2 file Split - 2 Cores", multi_processing, args, destination_file, num_tests)
    
    args = [5, 2] # 5 Files, 2 Cores Running
    speed_test("5 file Split - 2 Cores", multi_processing, args, destination_file, num_tests)

    args = [5, 3] # 5 Files, 3 Cores Running
    speed_test("5 file Split - 3 Cores", multi_processing, args, destination_file, num_tests)

    args = [5, 4] # 5 Files, 4 Cores Running
    speed_test("5 file Split - 4 Cores", multi_processing, args, destination_file, num_tests)

    args = [5, 5] # 5 Files, 5 Cores Running
    speed_test("5 file Split - 5 Cores", multi_processing, args, destination_file, num_tests)

    args = [10, 2] # 20 Files, 4 Cores Running
    speed_test("10 file Split - 2 Cores", multi_processing, args, destination_file, num_tests)

    args = [10, 3] # 20 Files, 3 Cores Running
    speed_test("10 file Split - 3 Cores", multi_processing, args, destination_file, num_tests)

    args = [10, 4] # 20 Files, 4 Cores Running
    speed_test("10 file Split - 4 Cores", multi_processing, args, destination_file, num_tests)

    args = [10, 5] # 20 Files, 4 Cores Running
    speed_test("10 file Split - 5 Cores", multi_processing, args, destination_file, num_tests)

    args = [20, 2] # 20 Files, 2 Cores Running
    speed_test("20 file Split - 2 Cores", multi_processing, args, destination_file, num_tests)

    args = [20, 3] # 20 Files, 3 Cores Running
    speed_test("20 file Split - 3 Cores", multi_processing, args, destination_file, num_tests)

    args = [20, 4] # 20 Files, 4 Cores Running
    speed_test("20 file Split - 4 Cores", multi_processing, args, destination_file, num_tests)

    args = [20, 5] # 20 Files, 5 Cores Running
    speed_test("20 file Split - 5 Cores", multi_processing, args, destination_file, num_tests)

    


    

       
if __name__ == '__main__' : main()