#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Queue:
    def __init__(self):
        self.list = LinkedList()
        
    def push(self, new_item):
        self.list.append(new_item)    # Insert as list tail (end of queue)
    
    def pop(self):
        popped_item = self.list.head   # Copy list head (front of queue)
        self.list.remove_after(None)   # Remove list head
        return popped_item             # Return popped item


class Vertex:
    def __init__(self, label):
        self.label = label
        self.distance = float("inf")   # Distance to graph's start vertex
        self.next = None
        self.pred_vertex = None # For Dijkstra's

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
    
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []
    
    def add_directed_edge(self, from_vertex, to_vertex, weight = 1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)
    
    def add_undirected_edge(self, vertex_a, vertex_b, weight = 1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # Returns the vertex in this graph with the specified label, or None
    # if no such vertex exists.
    def get_vertex(self, vertex_label):
        for vertex in self.adjacency_list:
            if vertex.label == vertex_label:
                return vertex
        return None
    
    # Returns a list of all vertices in this graph
    def get_vertex_list(self):
        return list(self.adjacency_list)

    # Returns a list of all edges incoming to the specified vertex
    # Each edge is a tuple of the form (from_vertex, to_vertex)
    def get_incoming_edges(self, vertex):
        incoming = []
        for edge in self.edge_weights:
            if edge[1] is vertex:
                incoming.append(edge)
        return incoming


class LinkedList:
   def __init__(self):
      self.head = None
      self.tail = None

   def append(self, new_node):
      if self.head == None:
         self.head = new_node
         self.tail = new_node
      else:
         self.tail.next = new_node
         self.tail = new_node

   def prepend(self, new_node):
      if self.head == None:
         self.head = new_node
         self.tail = new_node
      else:
         new_node.next = self.head
         self.head = new_node

   def insert_after(self, current_node, new_node):
      if self.head == None:
         self.head = new_node
         self.tail = new_node
      elif current_node is self.tail:
         self.tail.next = new_node
         self.tail = new_node
      else:
         new_node.next = current_node.next
         current_node.next = new_node
   
   def remove_after(self, current_node):
     # Special case, remove head
     if (current_node == None) and (self.head != None):
        succeeding_node = self.head.next
        self.head = succeeding_node  
        if succeeding_node == None:    # Removed last item
           self.tail = None
     elif current_node.next != None:
        succeeding_node = current_node.next.next
        current_node.next = succeeding_node
        if succeeding_node == None:    # Removed tail
           self.tail = current_node


class Queue:
    def __init__(self):
        self.list = LinkedList()
        
    def push(self, new_item):
        self.list.append(new_item)    # Insert as list tail (end of queue)
    
    def pop(self):
        popped_item = self.list.head   # Copy list head (front of queue)
        self.list.remove_after(None)   # Remove list head
        return popped_item             # Return popped item

