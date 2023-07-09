#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import threading
import os
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import queue
import threading
from os.path import exists
import shutil
import gc
import numpy as np
import sys
from filesplit.split import Split

def make_directory(dir):
    try:
        os.mkdir(dir)
    except OSError as exc:
        return

def clean_directory(result_file):
    if exists(result_file):
        os.remove(result_file)
    tmp = "tmp/"
    #if os.path.isdir(tmp):
    #    shutil.rmtree(tmp)
    for i in range(10):
        r = "hugefile1_" + str(i) +".txt"
        if exists(r):
            os.remove(r)
        
    pass



multiprocess_queue = queue.PriorityQueue()

def multiprocess_job(process_number,destination_file, thread_count, chunk_size, file_one, file_two, total_rows, directory, rows_per_file, chunk_row_count,split_by_rows):
    #process_count = 6
    processes = []
    mp_job_count = int(total_rows/split_by_rows)
    combine_queue = Queue()
    tmp_dir = "tmp/"
    make_directory(tmp_dir)
    combined_file_prefix = tmp_dir + "combined_file_"
    mt = Multithreading_solution()
    mt.chunk_row_count = chunk_row_count
    mt.lines_per_chunk = rows_per_file

    for job_num in range(process_number, mp_job_count):
        huge_file_one = directory + "bigfile1_" + str(job_num) +".txt"
        huge_file_two = directory + "bigfile2_" + str(job_num) +".txt"
        tmp_dir = "tmp_" + str(job_num) + "/"
        destination_file = combined_file_prefix + str(job_num) + ".txt"
        #Create Args
        args = [chunk_size, huge_file_one, huge_file_two, tmp_dir, destination_file, thread_count]
        #Place in MultiProcess Queue
        multiprocess_queue.put(args)
    while True:
        queue_size = multiprocess_queue.qsize()
        try:
            queue_item = multiprocess_queue.get(False)
        except:
            return
        else:
            chunk_size = queue_item[0] 
            file_one = queue_item[1]
            file_two = queue_item[2]
            tmp_dir = queue_item[3]
            destination_file = queue_item[4]
            thread_count = queue_item[5]
            mt.no_more_read_data = False
            mt.no_more_write_data = False
            mt.closed_files = []
            mt.docs_closed = 0
            mt.final_row_count = rows_per_file
            mt.lines_written = 0
            mt.execute(file_one, file_two, destination_file)

class Multiprocessing_solution():
    def __init__(self):
        pass

    def run(self, process_count,destination_file, thread_count, chunk_size, file_one, file_two, split_by_rows, total_rows, directory,final_row_count,chunk_row_count,rows_per_file):
        processes = []
        
        mp_job_count = int(total_rows/split_by_rows)
        
        combined_file_prefix = "tmp/combined_file_"
        
        for job_num in range(0,process_count):                  
            processes.append(Process(target=multiprocess_job, args=(job_num,destination_file, thread_count, chunk_size, file_one, file_two, total_rows, directory,rows_per_file,chunk_row_count,split_by_rows,), name='Process-'+str(job_num)))

        #Start MultiProcessing
        [p.start() for p in processes]
        [p.join() for p in processes]
        # Appending resulting files together    
        destination = open("totalfile.txt",'a')   
        for i in range(mp_job_count):
            source_file = combined_file_prefix + str(i) + ".txt"
            file_source = open(source_file, 'r')
            shutil.copyfileobj(file_source, destination)
            file_source.close()
            #os.remove(source_file)
        destination.close()
        pass

class Multithreading_solution():
    def __init__(self):
        self.docs_closed = 0
        self.read_queue_one = queue.PriorityQueue()
        self.read_queue_two = queue.PriorityQueue()
        self.write_queue = queue.PriorityQueue()
        self.no_more_read_data = False
        self.no_more_write_data = False
        self.chunk_size = 200000 #Bytes of data read threads grab at one time
        self.chunk_row_count = 25000 #Amount of rows to be written to file at one time.
        self.destination_file = "totalfile.txt"
        self.closed_files = []
        self.split_by_rows = 100000
        self.final_row_count = 100000
        self.lines_written = 0
   
    def read_thread(self, q,file_name):
        total_lines = 0
        priority=0
        f = open(file_name, "r")
        data = []
        no_more_read_data = False
        while True:
            while no_more_read_data == False:
                obtained_data = f.readlines(self.chunk_size)
                data = data + obtained_data
                if len(obtained_data) == 0:
                    no_more_read_data = True
                    pass
                if len(data) < self.chunk_row_count and no_more_read_data == False:
                    continue
                else:   
                    break
            while len(data) >= self.chunk_row_count:
                priority+=1
                item_data = np.asarray(data[:self.chunk_row_count],dtype=np.int64)
                data = data[self.chunk_row_count:]
                item = (priority, item_data)
                q.put(item)
            if no_more_read_data:
                break
            pass
        #Closing File
        f.close()
        self.closed_files.append(file_name)
        self.docs_closed+=1
        pass

    def get_item(self, read_q, read_file):
        while True:
            try:
                item = read_q.get(False)
            except:
                if self.lines_written == self.final_row_count:
                    return None
                else:
                    continue
            else:
                return item

    def process_thread(self, file_one, file_two):
        
        new_line = np.array(["\n"]).astype(str)
        while True:
            item_one = self.get_item(self.read_queue_one, file_one)
            if item_one == None:
                ##print("BREAKING ITEM 1")
                if self.no_more_read_data:
                    self.no_more_write_data = True
                    self.write_queue.put(None)
                    return
            item_two = self.get_item(self.read_queue_two, file_two)
            if item_two == None:
                ##print("BREAKING ITEM 2")
                if self.no_more_read_data:
                    self.no_more_write_data = True
                    #self.write_queue.put(None)
                    return
            if item_one == None and item_two == None:
                self.no_more_write_data = True
                ##print("PROCESS THREAD QUIT")
                return
            merged_data = np.add(item_one[1],item_two[1])
            merged_data = np.char.add(merged_data.astype(str),new_line).astype(str) 
         #   print("MERGED DATA LEN: ",len(merged_data))
            self.write_queue.put((item_one[0],merged_data.tolist()))

        
 
                
    def write_thread(self,destination_file, file_one, file_two):
        f = open(destination_file, "w")
        while True:
            queue_size = self.write_queue.qsize()
            if file_one in self.closed_files and file_two in self.closed_files and self.no_more_write_data and queue_size == 0 and self.final_row_count == self.lines_written:
                return
            if queue_size != 0:
                while True:
                    try:
                        data = self.write_queue.get(False)
                    except:
                        break
                        if self.docs_closed == 2 and self.no_more_write_data:
                            f.close()
                            return
                    else:
                        if data == None:
                            f.close()
                            return
                        len_data = len(data[1])
                        f.writelines(data[1])
                        self.lines_written +=len_data
                        data=[]
        queue_size = self.write_queue.qsize()
        f.close()
    
    def split(self,file_one,file_two,dir):
        dir = "bigfiles/"
        lines_per_file = 100000000
        make_directory(dir)
        start = time.time() # Start time of Multithreading
        split = Split(file_one, dir).bylinecount(lines_per_file)
        split = Split(file_two, dir).bylinecount(lines_per_file)
        end = time.time() # End time of executing function
        ms = (end-start) * 10**3
        pass
    
    def execute(self,file_one, file_two,destination_file):
        if exists(destination_file):
            return
        threads = []        
        threads.append(threading.Thread(target=self.read_thread, args=(self.read_queue_one,file_one,), name='read-thread_one'))
        threads.append(threading.Thread(target=self.read_thread, args=(self.read_queue_two,file_two,), name='read-thread_two'))
        threads.append(threading.Thread(target=self.process_thread, args=(file_one,file_two,), name='process-thread'))
        threads.append(threading.Thread(target=self.process_thread, args=(file_one,file_two,), name='process-thread'))
        threads.append(threading.Thread(target=self.write_thread, args=(destination_file,file_one,file_two,), name='write-thread'))
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        pass

def main():
    result_file = "totalfile.txt"
    clean_directory(result_file)

    x = Multithreading_solution()
    x.final_row_count=10000000
    x.chunk_row_count = 100000
    x.chunk_size = 50000 #Bytes of data for reader to grab at a time
    file_one = "10milfile1.txt"
    file_two = "10milfile2.txt"

    start = time.time()
    x.execute(file_one, file_two, result_file)
    end = time.time() # End time of executing function
    ms = (end-start) * 10**3
    print("Multithreading Completed in: ",ms)
   
    # x.split()
    mp = Multiprocessing_solution()

    clean_directory(result_file)

    file_one = "hugefile1.txt"
    file_two = "hugefile2.txt"
    
    directory = "bigfiles/"
    start = time.time()
    x.split(file_one,file_two,directory)
    end = time.time() # End time of executing function
    ms = (end-start) * 10**3
    print("Splitting files Completed in: ",ms)


    
     
    process_count = 6
    destination_file = "totalfile.txt"
    thread_count = 3
    chunk_size = 2000000

    total_rows = 1000000000 # total rows of the amount in the big text file
    final_row_count = 1000000000 # total rows of the amount in the big text file
    split_by_rows = 100000000
    chunk_row_count = 100000
    chunk_size = 2100000 #Bytes of data for reader to grab at a time
    rows_per_file = 100000000

    start = time.time()
    mp.run(process_count,destination_file, thread_count, chunk_size, file_one, file_two, split_by_rows, total_rows, directory, final_row_count,chunk_row_count,rows_per_file)
    end = time.time() # End time of executing function
    ms = (end-start) * 10**3
    print("Multiprocessing Completed in: ",ms)


if __name__ == '__main__' : main()