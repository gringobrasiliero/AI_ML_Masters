#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graph import Vertex, Graph, LinkedList, Queue




# Breadth-first search function
def breadth_first_search(graph, start_vertex):
    discovered_set = []
    frontier_queue = Queue()

    frontier_queue.push(start_vertex)      # Push start_vertex to frontier_queue
    discovered_set.append(start_vertex)    # Add start_vertex to discovered_set

    while (frontier_queue.list.head is not None):    # While the queue is not empty
        current_vertex = frontier_queue.pop()    # current_vertex is currently visited      
        for adjacent_vertex in graph.adjacency_list[current_vertex]:
           if(discovered_set.count(adjacent_vertex) == 0):
               frontier_queue.push(adjacent_vertex)
               discovered_set.append(adjacent_vertex)
                # Distance of adjacent_vertex is 1 more than current_vertex
               adjacent_vertex.distance = current_vertex.distance + 1
    return discovered_set


def example_breadth_first_search():
    # Main program
    g = Graph()
    vertex_a = Vertex('Joe')
    vertex_b = Vertex('Eva')
    vertex_c = Vertex('Taj')
    vertex_d = Vertex('Chen')
    vertex_e = Vertex('Lily')
    vertex_f = Vertex('Jun')
    vertex_g = Vertex('Ken')
    vertices = [vertex_a, vertex_b, vertex_c, vertex_d, vertex_e, vertex_f, vertex_g]

    g.add_vertex(vertex_a)
    g.add_vertex(vertex_b)
    g.add_vertex(vertex_c)
    g.add_vertex(vertex_d)
    g.add_vertex(vertex_e)
    g.add_vertex(vertex_f)
    g.add_vertex(vertex_g)
    
    # Building graph
    g.add_undirected_edge(vertex_a, vertex_b)  # Edge from Joe to Eva
    g.add_undirected_edge(vertex_a, vertex_c)  # Edge from Joe to Taj
    g.add_undirected_edge(vertex_b, vertex_e)  # Edge from Eva to Lily
    g.add_undirected_edge(vertex_c, vertex_d)  # Edge from Taj to Chen
    g.add_undirected_edge(vertex_c, vertex_e)  # Edge from Taj to Lily
    g.add_undirected_edge(vertex_d, vertex_f)  # Edge from Chen to Jun
    g.add_undirected_edge(vertex_e, vertex_f)  # Edge from Lily to Jun
    g.add_undirected_edge(vertex_f, vertex_g)  # Edge from Jun to Ken

    start_name = input('Enter the starting person\'s name: ')
    print()

    for vertex in vertices:
        if vertex.label == start_name:
            start_vertex = vertex

    discovered_set = breadth_first_search(g, start_vertex)

    # Output
    print('Breadth-first search traversal')
    print('Start vertex: %s' % start_vertex.label)
    for vertex in discovered_set:
        print('%s: %d' % (vertex.label, vertex.distance))
    

def main():
    example_breadth_first_search()


if __name__ == '__main__' : main()



