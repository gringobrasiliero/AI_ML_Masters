
from graph import Vertex, Graph
from display_matrix import display_matrix

# Implementation of Floyd-Warshall all-pairs shortest path
def all_pairs_shortest_path(graph):
    vertices = graph.get_vertex_list()
    num_vertices = len(vertices)

    # Initialize dist_matrix to a num_vertices x num_vertices matrix 
    # with all values set to infinity
    dist_matrix = []
    for i in range(0, num_vertices):
        dist_matrix.append([float("inf")] * num_vertices)

    # Set each distance for vertex to same vertex to 0
    for i in range(0, num_vertices):
        dist_matrix[i][i] = 0

    # Finish matrix initialization
    for edge in graph.edge_weights:
        dist_matrix[vertices.index(edge[0])][vertices.index(edge[1])] = graph.edge_weights[edge]

    # Loop through vertices
    for k in range(0, num_vertices):
        for toIndex in range(0, num_vertices):
            for fromIndex in range(0, num_vertices):
                currentLength = dist_matrix[fromIndex][toIndex]
                possibleLength = dist_matrix[fromIndex][k] + dist_matrix[k][toIndex]
                if possibleLength < currentLength:
                    dist_matrix[fromIndex][toIndex] = possibleLength

    return dist_matrix

# Path reconstruction function
def reconstruct_path(graph, start_vertex, end_vertex, dist_matrix):
    vertices = graph.get_vertex_list()
    start_index = vertices.index(start_vertex)
    path = []
    
    # Backtrack from the ending vertex
    current_index = vertices.index(end_vertex)
    while current_index != start_index:
        incoming_edges = graph.get_incoming_edges(vertices[current_index])
        
        found_next = False
        for current_edge in incoming_edges:
            expected = dist_matrix[start_index][current_index] - graph.edge_weights[current_edge]
            actual = dist_matrix[start_index][vertices.index(current_edge[0])]
            if expected == actual:
                # Update current vertex index
                current_index = vertices.index(current_edge[0])
                
                # Prepend current_edge to path
                path = [current_edge] + path
                
                # The next vertex in the path was found
                found_next = True
                
                # The correct incoming edge was found, so break the inner loop
                break

        if found_next == False:
            return None # no path exists

    return path


# Main program

graphs = [
    # Graph 1
    (["A", "B", "C", "D"],
     [("A", "B", 2), ("B", "C", -3), ("B", "D", 7), ("C", "A", 5), ("D", "A", -4)],
     "C", "D" # show path from C to D
    ),
          
    # Graph 2
    (["A", "B", "C", "D"],
     [("A", "B", 4), ("B", "C", 3), ("C", "D", 6), ("D", "A", -1), ("D", "B", 7)],
     "D", "B" # show path from D to B
    ),
          
    # Graph 3
    (["A", "B", "C"],
     [("A", "B", 1), ("A", "C", 1), ("B", "C", -8)],
     "C", "A" # show path from C to A (no path)
    ),
          
    # Graph 4
    (["A", "B", "C", "D", "E"],
     [("A", "B", 1), ("A", "E", 8), ("B", "C", 2), ("C", "D", 3), ("D", "A", -5), ("E", "D", 9)],
     "A", "D" # show path from A to D
    )
]

# Run samples for each graph defined above
graph_number = 1
for graph_desc in graphs:
    graph = Graph()

    # Add vertices
    vertex_names = graph_desc[0]
    for vertex_name in vertex_names:
        graph.add_vertex(Vertex(vertex_name))
    # Add edges
    edge_tuples = graph_desc[1]
    for edge_tuple in edge_tuples:
        graph.add_directed_edge(graph.get_vertex(edge_tuple[0]), graph.get_vertex(edge_tuple[1]), edge_tuple[2])

    # Get the matrix for all pairs shortest path
    matrix = all_pairs_shortest_path(graph)

    # Display the matrix
    print("All-pairs shortest path matrix (graph %d):" % graph_number)
    display_matrix(matrix)

    # Show an actual path sequence
    print("Shortest path from %s to %s:" % (graph_desc[2], graph_desc[3]))
    start_vertex = graph.get_vertex(graph_desc[2])
    end_vertex = graph.get_vertex(graph_desc[3])
    path = reconstruct_path(graph, start_vertex, end_vertex, matrix)
    if path is None or len(path) == 0:
        print("No path")
    else:
        print(path[0][0].label, end="")
        for edge in path:
            print(" to " + str(edge[1].label), end="")
        print()
    print()

    # Increment graph number for next example
    graph_number = graph_number + 1
