#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def create_list(list_length):
    list = []
    for i in range(list_length):
        num = random.randint(0,1000)
        list.append(num)
    return list

def minimum_number_On(list):
    min_number = list[0]
    for number in list[1:]:
        if number < min_number:
            min_number = number
    return min_number

def minimum_number_On_squared(list):
    i= 0
    list_length = len(list)
    smallest_number = list[0]
    while i < list_length:
        num = list[i]
        smallest_num = True
        j = 0
        while j < list_length:
            compare_num = list[j]
            if compare_num < num:
                smallest_num = False
            j+=1
        if smallest_num:
            smallest_number = num
        i+=1
    return smallest_number

def main():    
    list = create_list(10)
    print(list)
    min_number = minimum_number_On(list)    
    min_number_two = minimum_number_On_squared(list)
    print("Minimum Number from O(n) Algorithm: " + str(min_number))
    print("Minimum Number from O(n^2) Algorthm: " + str(min_number_two))
    pass

if __name__ == '__main__' : main()

