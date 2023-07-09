#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time


class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class Linked_list():
    def __init__(self):
        self.head = None
        self.tail = None

    #Places Node at the Tail of the List
    def append(self, node):
        if self.head == None: #List is Empty
            self.head = node
            self.tail = node
        else:
            #Last Nodes next is the new node
            self.tail.next = node
            #The New Nodes Prev is the current Tail
            node.prev = self.tail
            #The New Node is now the tail
            self.tail = node


    #Places Node at the Head of the List
    def prepend(self, node):
        if self.head == None: #List is Empty
            self.head = node
            self.tail = node
        else:
            #New Node's Next is Current Head
            node.next = self.head
            #Current Head's Prev is the new Node
            self.head.prev = node
            #The New Node is now the head
            self.head = node



    def remove(self, node):
        next_node = node.next
        prev_node = node.prev

        if next_node != None:
            next_node.prev = prev_node
        if prev_node != None:
            prev_node.next = next_node
        if node == self.head:
            self.head = next_node
        if node == self.tail:
            self.tail = prev_node
    pass

class Stack():
    def __init__(self):
        self.list = Linked_list()
        pass

    def push(self,data):
        node = Node(data)
        #Prepend Node to Head (Top of the stack)
        self.list.prepend(node)

    def pop(self):
        pop_item = self.list.head
        #Pop List Head
        #self.list.remove_after(None)
        self.list.remove(pop_item)
        return pop_item
    
    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None


class Queue():
    def __init__(self):
        self.list = Linked_list()
        pass

    def push(self, value):
        node = Node(value)
        #Append Node to Tail (Back of the Line)
        self.list.append(node)
    
    def pop(self):
        pop_item = self.list.head
        #Pop List Head
        self.list.remove(pop_item)
        return pop_item

    def peek(self):
        if self.size != 0:
            return self.items[0]
        else:
            return None

class List_based_queue():
    def __init__(self):
        self.list = []
        pass
    def push(self, item):
        self.list.append(item)
        pass
    def pop(self):
        #Removing First Index of List
        return self.list.pop(0)
    pass

class List_based_stack():
    def __init__(self):
        self.list = []
        pass
    def push(self, item):
        self.list.append(item)
        pass
    def pop(self):
        #Removing Last Index of List
        return self.list.pop()
    pass


def create_list(list_length):
    list = []
    for i in range(list_length):
        num = random.randint(0,1000)
        list.append(num)
    return list


def performance_test(list, obj, obj_name):
    queue = obj
    list_len = len(list)

    se = time.time() # Start time of Pushing begins here
    for item in list:
        obj.push(item)
    ee = time.time() # End Time of Pushing 
    print("Number of ms it took to push " + str(list_len) + " items into the " + obj_name + ":",(ee-se) * 10**3, "ms")

    se = time.time() # Start time of Popping begins here
    for i in range(list_len):
        obj.pop()
    ee = time.time() # End time of Popping
    print("Number of ms it took to pop " + str(list_len) + " items from the " + obj_name + ":",(ee-se) * 10**3, "ms")
    print()


def main():
    list = create_list(500000)
  
    list_based_stack = List_based_stack()
    performance_test(list, list_based_stack, "List Based Stack")

    list_based_queue = List_based_queue()
    performance_test(list, list_based_queue, "List Based Queue")


    stack = Stack()
    performance_test(list, stack, "Doubly Linked List Based Stack")

    queue = Queue()
    performance_test(list, queue, "Doubly Linked List Based Queue")

    pass

if __name__ == '__main__' : main()





