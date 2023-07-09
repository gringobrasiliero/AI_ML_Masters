
from graph import Vertex, Graph

def bellman_ford(graph, start_vertex):
    # Initialize all vertex distances to infinity and
    # and predecessor vertices to None.
    for current_vertex in graph.adjacency_list:
      current_vertex.distance = float('inf') # Infinity
      current_vertex.pred_vertex = None

    # start_vertex has a distance of 0 from itself
    start_vertex.distance = 0                

    # Main loop is executed |V|-1 times to guarantee minimum distances.
    for i in range(len(graph.adjacency_list)-1):
        # The main loop.
        for current_vertex in graph.adjacency_list:
            for adj_vertex in graph.adjacency_list[current_vertex]:
                edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight
                      
                # If shorter path from start_vertex to adj_vertex is found,
                # update adj_vertex's distance and predecessor
                if alternative_path_distance < adj_vertex.distance:
                   adj_vertex.distance = alternative_path_distance
                   adj_vertex.pred_vertex = current_vertex

    # Check for a negative edge weight cycle
    for current_vertex in graph.adjacency_list:
        for adj_vertex in graph.adjacency_list[current_vertex]:
             edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
             alternative_path_distance = current_vertex.distance + edge_weight

             # If shorter path from start_vertex to adj_vertex is still found,
             # a negative edge weight cycle exists
             if alternative_path_distance < adj_vertex.distance:
                return False

    return True

def get_shortest_path(graph, start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    distance = 0.0
    while current_vertex is not start_vertex:
        if current_vertex is None:
            return ("No path")
        path = " -> " + str(current_vertex.label) + path
        if current_vertex.pred_vertex is not None:
            distance += graph.edge_weights[(current_vertex.pred_vertex, current_vertex)]
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path + " (%g)" % distance
    return path

if __name__ == "__main__":
    g = Graph()
    
    vertex_A = Vertex("A")
    vertex_B = Vertex("B")
    vertex_C = Vertex("C")
    vertex_D = Vertex("D")
    vertex_E = Vertex("E")
    vertex_F = Vertex("F")
    
    g.add_vertex(vertex_A)
    g.add_vertex(vertex_B)
    g.add_vertex(vertex_C)
    g.add_vertex(vertex_D)
    g.add_vertex(vertex_E)
    g.add_vertex(vertex_F)

    g.add_directed_edge(vertex_A, vertex_B, 1)
    g.add_directed_edge(vertex_A, vertex_C, 2)
    g.add_undirected_edge(vertex_B, vertex_C, 1)
    g.add_undirected_edge(vertex_B, vertex_D, 3)
    g.add_directed_edge(vertex_B, vertex_E, 2)
    g.add_undirected_edge(vertex_C, vertex_E, 2)
    g.add_directed_edge(vertex_D, vertex_C, 1)
    g.add_undirected_edge(vertex_D, vertex_E, 4)
    g.add_directed_edge(vertex_D, vertex_F, 3)
    g.add_directed_edge(vertex_E, vertex_F, 3)

    # Set starting vertex for shortest paths.
    start_vertex = vertex_A

    # Run Bellman-Ford's shortest path algorithm. Display results if
    # successful, or error message if a negative edge weight cycle exists.
    if bellman_ford(g, start_vertex):
        # No negative edge weight cycles. Print shortest path information from
        # start_vertex to each other vertex in the graph.
        for v in g.adjacency_list:
            path = get_shortest_path(g, start_vertex, v)
            print("%s -> %s: %s" % (start_vertex.label, v.label, path))
    else:
        print("Bellman-Ford failed, negative edge weight cycle detected.")
