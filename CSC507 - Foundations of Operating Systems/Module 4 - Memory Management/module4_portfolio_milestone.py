#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import time
import os


def method_one():
    with open("file1.txt", 'r') as read_file:
        file_one_contents = read_file.readlines()
        print(type(file_one_contents))
    with open("newfile1.txt",'w') as write_file:
        for i in range(0,len(file_one_contents)):
            file_one_num = int(file_one_contents[i].strip())
            doubled_num = file_one_num * 2
            write_file.write(str(doubled_num) + "\n")
    pass


def method_two():
    with open("file1.txt", 'r') as read_file:
        with open("newfile1.txt",'w') as write_file:
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


def speed_test(test_name, test_function, txt_file_name, num_tests):
    execution_times = []
    for i in range(num_tests):
        start = time.time() # Start time of executing function
        test_function()
        end = time.time() # End time of executing function
        ms = (end-start) * 10**3
        execution_times.append(ms)
        os.remove(txt_file_name)
    average_milliseconds = sum(execution_times) / len(execution_times)
    print("Average Execution time of " + test_name + " is " +  str(average_milliseconds) + " ms.")


def main():
    txt_file_name = "newfile1.txt"

    speed_test("Method_One", method_one, txt_file_name, 10)
    speed_test("Method_Two", method_two, txt_file_name, 10)
    speed_test("Method_Three", method_three, txt_file_name, 10)
       
if __name__ == '__main__' : main()