#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Binary max heap percolate down
def max_heap_percolate_down(node_index, heap_list, list_size):
    child_index = 2 * node_index + 1
    value = heap_list[node_index]

    while child_index < list_size:
        # Find the max among the node and all the node's children
        max_value = value
        max_index = -1
        i = 0
        while i < 2 and i + child_index < list_size:
            child_val = heap_list[i + child_index]
            if child_val > max_value:
                max_value = heap_list[i + child_index]
                max_index = i + child_index
            i = i + 1
                                    
        if max_value == value:
            return

        # Swap heap_list[node_index] and heap_list[max_index]
        temp = heap_list[node_index]
        heap_list[node_index] = heap_list[max_index]
        heap_list[max_index] = temp
        
        node_index = max_index
        child_index = 2 * node_index + 1


# Sorts the list of numbers using the heap sort algorithm
def heap_sort(numbers):
    # Heapify numbers list
    i = len(numbers) // 2 - 1
    while i >= 0:
        max_heap_percolate_down(i, numbers, len(numbers))
        i = i - 1
    print(numbers)
    i = len(numbers) - 1
    while i > 0:
        # Swap numbers[0] and numbers[i]
        temp = numbers[0]
        numbers[0] = numbers[i]
        numbers[i] = temp

        max_heap_percolate_down(0, numbers, i)
        print(numbers)
        i = i - 1
    return numbers


def main():
    list = [25, 44, 55, 99, 30, 37, 15, 10, 2, 4]
    print(list)
    list = heap_sort(list)
    print(list)

# Driver Code
if __name__ == "__main__": main()
      
   
    
  
    
