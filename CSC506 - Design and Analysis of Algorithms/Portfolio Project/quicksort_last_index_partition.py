#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import pandas as pd

class Quick_sort():
    def __init__(self):
        self.name = "Quick Sort"
        pass
    def sort(self, list):
        list_len = len(list)-1
        return self.quicksort(list, 0, list_len)

    def quicksort(self, list, first, last):
        if first < last:
            pivotID = self.partition(list, first, last)
            #Sort the partitions
            list = self.quicksort(list, first, pivotID-1)
            list = self.quicksort(list, pivotID+1, last)
        return list

    def partition(self, list, first, last):
        last_index = int(last)
        pivot = list[last_index] #Selecting last index as pivot point 
        done = False
        while not done:
            while list[first] < pivot:
                first += 1
            while list[last] > pivot:
                last-=1
            if first >= last:
                done = True
            else:  
                temp = list[first]
                list[first]=list[last]
                list[last]=temp
                first +=1
                last -=1
        return last

def create_decreasing_list(list_length):
    list = []
    for i in range(list_length,0,-1):
        list.append(i)
    return list

def main():
    list = create_decreasing_list(997)
    print(list)
    sort = Quick_sort()
    sort.sort(list)
    print(list)
    pass

if __name__ == '__main__':  
    main()
