#!/usr/bin/env python
# -*- coding: utf-8 -*-


from graph import Vertex, Graph

# Depth-first search function
def depth_first_search(graph, start_vertex, visit_function):
    vertex_stack = [start_vertex]
    visited_set = set()

    while len(vertex_stack) > 0:
        current_vertex = vertex_stack.pop()
        if current_vertex not in visited_set:
            visit_function(current_vertex)
            visited_set.add(current_vertex)
            for adjacent_vertex in graph.adjacency_list[current_vertex]:
                vertex_stack.append(adjacent_vertex)


# Main program - Creates 3 different graphs, each with vertices A through F, but with 
# different sets of edges. Traverses each with DFS.
vertex_names = ["A", "B", "C", "D", "E", "F"]

# Add the same set of vertices to 3 different graphs
graph1 = Graph()
graph2 = Graph()
graph3 = Graph()
graphs = [graph1, graph2, graph3]
for vertex_name in vertex_names:
    for graph in graphs:
        graph.add_vertex(Vertex(vertex_name))

# Add graph 1's edges
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("B"))
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("D"))
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("E"))
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("F"))
graph1.add_undirected_edge(graph1.get_vertex("C"), graph1.get_vertex("F"))
graph1.add_undirected_edge(graph1.get_vertex("E"), graph1.get_vertex("F"))

# Add graph 2's edges
graph2.add_undirected_edge(graph2.get_vertex("A"), graph2.get_vertex("B"))
graph2.add_undirected_edge(graph2.get_vertex("B"), graph2.get_vertex("C"))
graph2.add_undirected_edge(graph2.get_vertex("C"), graph2.get_vertex("F"))
graph2.add_undirected_edge(graph2.get_vertex("D"), graph2.get_vertex("E"))
graph2.add_undirected_edge(graph2.get_vertex("E"), graph2.get_vertex("F"))

# Add graph 3's edges
graph3.add_undirected_edge(graph3.get_vertex("A"), graph3.get_vertex("B"))
graph3.add_undirected_edge(graph3.get_vertex("A"), graph3.get_vertex("E"))
graph3.add_undirected_edge(graph3.get_vertex("B"), graph3.get_vertex("C"))
graph3.add_undirected_edge(graph3.get_vertex("B"), graph3.get_vertex("E"))
graph3.add_undirected_edge(graph3.get_vertex("C"), graph3.get_vertex("E"))
graph3.add_undirected_edge(graph3.get_vertex("D"), graph3.get_vertex("E"))
graph3.add_undirected_edge(graph3.get_vertex("E"), graph3.get_vertex("F"))

# Create a visitor function that displays a vertex's label
visitor = lambda x: print(x.label, end=' ')

# Choose a starting vertex
start_vertex_label = "A"

# Visit vertices in each graph with DFS
print('Depth-first search traversal')
for i in range(0, len(graphs)):
    print('Graph ' + str(i + 1) + ': ', end='')
    depth_first_search(graphs[i], graphs[i].get_vertex(start_vertex_label), visitor)
    print()