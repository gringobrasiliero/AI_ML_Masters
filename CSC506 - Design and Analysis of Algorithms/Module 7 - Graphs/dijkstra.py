#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
from graph import Graph, Vertex

def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:
        
        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight
                  
            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
                
def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path

        
# Program to find shortest paths from vertex A.
g = Graph()

vertex_a = Vertex("A")
vertex_b = Vertex("B")
vertex_c = Vertex("C")
vertex_d = Vertex("D")
vertex_e = Vertex("E")
vertex_f = Vertex("F")
vertex_g = Vertex("G")
g.add_vertex(vertex_a)
g.add_vertex(vertex_b)
g.add_vertex(vertex_c)
g.add_vertex(vertex_d)
g.add_vertex(vertex_e)
g.add_vertex(vertex_f)
g.add_vertex(vertex_g)

g.add_undirected_edge(vertex_a, vertex_b, 8)
g.add_undirected_edge(vertex_a, vertex_c, 7)
g.add_undirected_edge(vertex_a, vertex_d, 3)
g.add_undirected_edge(vertex_b, vertex_e, 6)
g.add_undirected_edge(vertex_c, vertex_d, 1)
g.add_undirected_edge(vertex_c, vertex_e, 2)
g.add_undirected_edge(vertex_d, vertex_f, 15)
g.add_undirected_edge(vertex_d, vertex_g, 12)
g.add_undirected_edge(vertex_e, vertex_f, 4)
g.add_undirected_edge(vertex_f, vertex_g, 1)

# Run Dijkstra's algorithm first.
dijkstra_shortest_path(g, vertex_a)

# Sort the vertices by the label for convenience; display shortest path for each vertex
# from vertex_a.    
for v in sorted(g.adjacency_list, key=operator.attrgetter("label")):
    if v.pred_vertex is None and v is not vertex_a:
        print("A to %s: no path exists" % v.label)
    else:
        print("A to %s: %s (total weight: %g)" % (v.label, get_shortest_path(vertex_a, v), v.distance))
