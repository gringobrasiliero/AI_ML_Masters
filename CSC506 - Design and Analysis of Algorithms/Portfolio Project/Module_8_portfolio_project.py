#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import pandas as pd

def create_random_list(list_length):
    list = []
    for i in range(list_length):
        num = random.randint(0,list_length)
        list.append(num)
    return list

def create_decreasing_list(list_length):
    list = []
    for i in range(list_length,0,-1):
        list.append(i)
    return list

def create_increasing_list(list_length):
    list = []
    for i in range(list_length):
        list.append(i)
    return list

class Timsort():
    def __init__(self):
        self.name = "Tim Sort"
        self.min_run = 32
        self.merge_sort = Merge_sort()
        self.insertion_sort = Insertion_sort()
        pass

    def sort(self, list):
        list_length = len(list)
        self.min_run = self.calculateMinimumRun(list_length)
        for i in range(0, list_length, self.min_run):
            #Insertion Sort
            self.insertion_sort.insertion_sort(list, i, min((i + self.min_run - 1), list_length - 1))           
        size = self.min_run
        while size < list_length:
            for start in range(0, list_length, size * 2):
                midpoint = start + size -1
                end = min((start + size * 2 - 1), (list_length-1))
                #Merge
                merged_list = self.merge_sort.merge(list[start:midpoint+1], list[midpoint+1:end+1])
                list[start:start+len(merged_list)] = merged_list
            size *=2
        return list

    def calculateMinimumRun(self, n):
        r = 0
        while n >= 32:
            r |= n & 1
            n >>= 1
        return n + r

class Merge_sort():
    def __init__(self):
        self.name = "Merge Sort"
        pass

    def sort(self, list):
        if len(list) < 2:
            return list
        midpoint = len(list) // 2
        return self.merge(self.sort(list[:midpoint]), self.sort(list[midpoint:]))

    def merge(self, left, right):
        if len(left) == 0:
            return right
        elif len(right) == 0:
            return left

        result = []
        left_index = 0
        right_index = 0
        length_of_left = len(left)
        length_of_right = len(right)
        length_of_left_right = length_of_left + length_of_right

        i = 0
        while i < length_of_left_right:

            if left[left_index] <= right[right_index]:
                result.append(left[left_index])
                left_index += 1
            
            else:
                result.append(right[right_index])
                right_index += 1
            
            if right_index == length_of_right:
                    result += left[left_index:]
                    return result
            elif left_index == length_of_left:
                    result += right[right_index:]
                    return result
            i+=1

class Quick_sort():
    def __init__(self):
        self.name = "Quick Sort"
        pass
    def sort(self, list):
        list_len = len(list)-1
        return self.quicksort(list, 0, list_len)

    def quicksort(self, list, first, last):
        if first < last:
            #Calc Split Point
            pivotID = self.partition(list, first, last)
            #Sort the partitions
            list = self.quicksort(list, first, pivotID)
            list = self.quicksort(list, pivotID+1, last)
        return list

    def partition(self, list, first, last):
        midpoint = int(first + (last-first) / 2)
        pivot = list[midpoint]
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

class Insertion_sort():
    def __init__(self):
        self.name = "Insertion Sort"
        pass
    
    def sort(self, list):
        self.insertion_sort(list, 0, len(list)-1)
        return list

    def insertion_sort(self, list, first, last):
        for i in range(first+1, last+1):
           value = list[i]
           j = i
           while j > first and list[j-1] > value:
               list[j]=list[j-1]
               j-=1
           list[j]=value
        return list

def accuracy_test(sort_type):
    random_list = [3, 1,  4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5, 0, 2, 8, 8, 4, 1, 9, 7, 1, 6, 9, 3, 9, 9, 3, 7, 5, 1, 0]
    sorted_random_list = [0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9]
    random_list = sort_type.sort(random_list)
    if random_list == sorted_random_list:
        print(sort_type.name + " Test: Pass")
        return True
    else:
        print(sort_type.name + " Test: FAIL")
        print("Expected: " + str(sorted_random_list))
        print("Returned: " + str(random_list))
        return False

def speed_test(sort_type, list_order, small_list, medium_list, large_list):
    test_name = sort_type.name + " - " + list_order + " List"

    start = time.time() # Start time of Small Sort
    sort_type.sort(small_list)
    end = time.time() # End Time of Small Sort 
    ms_small = (end-start) * 10**3
    print(test_name + " - Small: " + str(ms_small) + " ms")
    
    start = time.time() # Start time of Medium Sort
    sort_type.sort(medium_list)
    end = time.time() # End Time of Medium Sort
    ms_medium = (end-start) * 10**3
    print(test_name + " - Medium: " + str(ms_medium) + " ms")
    
    start = time.time() # Start time of Large Sort
    sort_type.sort(large_list)
    end = time.time() # End Time of Large Sort
    ms_large = (end-start) * 10**3
    print(test_name + " - Large: " + str(ms_large) + " ms\n")
    
    res = [test_name, ms_small, ms_medium, ms_large]
    return res
    
def main():
    data = []
    insertion_sort = Insertion_sort()
    tim_sort = Timsort()
    merge_sort = Merge_sort()
    quick_sort = Quick_sort()

    #TESTING FOR CORRECT SORT
    print("ACCURACY TEST")
    accuracy_test(tim_sort)
    accuracy_test(merge_sort)
    accuracy_test(quick_sort)
    accuracy_test(insertion_sort)
    
    #print() #Printing extra line to separate Accuracy test results with Speed test results
    print("\nSPEED TEST")
    #INCREASING
    small_list = create_increasing_list(1000)
    medium_list = create_increasing_list(10000)
    large_list = create_increasing_list(100000)
    increasing_timsort_results = speed_test(tim_sort, "Increasing", small_list.copy(), medium_list.copy(), large_list.copy())
    increasing_merge_sort_results = speed_test(merge_sort, "Increasing", small_list.copy(), medium_list.copy(), large_list.copy())
    increasing_quick_sort_results = speed_test(quick_sort, "Increasing", small_list.copy(), medium_list.copy(), large_list.copy())
    increasing_insertion_sort_results = speed_test(insertion_sort, "Increasing", small_list.copy(), medium_list.copy(), large_list.copy())

    data.append(increasing_timsort_results)
    data.append(increasing_merge_sort_results)
    data.append(increasing_quick_sort_results)
    data.append(increasing_insertion_sort_results)
   

    #DECREASING
    small_list = create_decreasing_list(1000)
    medium_list = create_decreasing_list(10000)
    large_list = create_decreasing_list(100000)

    decreasing_timsort_results = speed_test(tim_sort, "Decreasing", small_list.copy(), medium_list.copy(), large_list.copy())
    decreasing_merge_sort_results = speed_test(merge_sort, "Decreasing", small_list.copy(), medium_list.copy(), large_list.copy())
    decreasing_quick_sort_results = speed_test(quick_sort, "Decreasing", small_list.copy(), medium_list.copy(), large_list.copy())
    decreasing_insertion_sort_results = speed_test(insertion_sort, "Decreasing", small_list.copy(), medium_list.copy(), large_list.copy())
    
    data.append(decreasing_timsort_results)
    data.append(decreasing_merge_sort_results)
    data.append(decreasing_quick_sort_results)
    data.append(decreasing_insertion_sort_results)
                
    #RANDOM
    small_list = create_random_list(1000)
    medium_list = create_random_list(10000)
    large_list = create_random_list(100000)

    random_timsort_results = speed_test(tim_sort, "Random", small_list.copy(), medium_list.copy(), large_list.copy())
    random_merge_sort_results = speed_test(merge_sort, "Random", small_list.copy(), medium_list.copy(), large_list.copy())
    random_quick_sort_results = speed_test(quick_sort, "Random", small_list.copy(), medium_list.copy(), large_list.copy())
    random_insertion_sort_results = speed_test(insertion_sort, "Random", small_list.copy(), medium_list.copy(), large_list.copy())
    
    data.append(random_timsort_results)
    data.append(random_merge_sort_results)
    data.append(random_quick_sort_results)
    data.append(random_insertion_sort_results)

    #Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['Name', 'Small List (1000)', 'Medium List (10,000)', 'Large List (100,000)'])  
    df.to_csv("results.csv")
    pass

if __name__ == '__main__':  
    main()
    

