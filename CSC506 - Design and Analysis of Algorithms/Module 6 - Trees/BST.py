#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TreePrint import pretty_tree


class Node():
    def __init__(self, data):
        self.data = data
        self.left_child = None
        self.right_child = None


class Binary_search_tree():
    def __init__(self, arr):
        arr = [*set(arr)] #Removes Duplicates
        self.root_node = self.build_tree(arr) 
        pass

    def __str__(self):
        return pretty_tree(self)

    def build_tree(self, arr):
        if not arr:
            return None
        arr.sort() #Sort Array
        middle_index = len(arr)//2

        left_arr = arr[:middle_index]
        right_arr = arr[middle_index+1:]

        node = Node(arr[middle_index]) 
        node.left_child = self.build_tree(left_arr)
        node.right_child = self.build_tree(right_arr)
        return node

    def insert(self, node):
        current_node = self.root_node
        while current_node != None:
            if node.data < current_node.data:
                if current_node.left_child == None:
                    current_node.left_child = node
                    current_node = None
                else:
                    current_node = current_node.left_child
            else:
                if current_node.right_child == None:
                    current_node.right_child = node
                    current_node = None
                else:
                    current_node = current_node.right_child
                    

    def delete(self, data):
        current_node = self.root_node
        parent = None
        while current_node != None:
            if current_node.data == data: 
                if current_node.left_child == None and current_node.right_child == None: #Removing Leaf Node
                    if parent == None:
                        self.root_node = None
                    elif parent.left_child == current_node:
                        parent.left_child = None
                    else:
                        parent.right_child = None
                    return # Node found and removed
                elif current_node.left_child != None and current_node.right_child == None:  # Removing Node with Left Child
                    if parent is None: # Node is root
                        self.root = current_node.left_child
                    elif parent.left_child is current_node: 
                        parent.left_child = current_node.left_child
                    else:
                        parent.right_child = current_node.left_child
                    return  # Node found and removed
                elif current_node.left_child == None and current_node.right_child != None:  # Removing Node with Right Child
                    if parent is None: # Node is root
                        self.root = current_node.right_child
                    elif parent.left_child == current_node:
                        parent.left_child = current_node.right_child
                    else:
                        parent.right_child = current_node.right_child
                    return  # Node found and removed
                else: #Removing Node with Both Left and Right Child
                    successor = current_node.right_child
                    while successor.left_child != None:
                        successor = successor.left_child
                    current_node.data = successor.data
                    parent = current_node
                    current_node = current_node.right_child
                    data = parent.data
            elif current_node.data < data:
                parent = current_node
                current_node = current_node.right_child
            else:
                parent = current_node
                current_node = current_node.left_child
        #Node Not Found
        return






def main():
    list = [1, 7, 4, 23, 8, 9, 4, 3, 5, 7, 9, 67, 6345, 324]
    tree= Binary_search_tree(list)
    print("Binary Search Tree after initialization:")
    print(tree)
    print("Binary Search Tree after Inserting a Node:")
    tree.insert(Node(123))
    print(tree)
    print("Binary Search Tree after Removing a Node:")
    tree.delete(67)
    print(tree)
    pass


if __name__ == '__main__' : main()
