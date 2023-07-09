#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HashItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    def __init__(self):
        self.size = 256
        self.slots =  [None for i in range(self.size)]
        self.count = 0
    
    def _hash(self, key): 
        mult = 1 
        hv = 0 
        for ch in key: 
            hv += mult * ord(ch) 
            mult += 1 
        return hv % self.size 


def main():

    pass

if __name__ == '__main__' : main()
