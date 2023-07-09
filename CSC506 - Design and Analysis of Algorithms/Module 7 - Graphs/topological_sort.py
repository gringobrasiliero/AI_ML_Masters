

from graph import Graph, Vertex

def get_incoming_edge_count(edge_list, vertex):
   count = 0
   for (from_vertex, to_vertex) in edge_list:
      if to_vertex is vertex:
         count = count + 1
   return count

def topological_sort(graph):
    result_list = []

    # make list of vertices with no incoming edges.
    no_incoming = []
    for vertex in graph.adjacency_list.keys():
        if get_incoming_edge_count(graph.edge_weights.keys(), vertex) == 0:
            no_incoming.append(vertex)
    
    # remaining_edges starts with all edges in the graph.
    # A set is used for its efficient remove() method.
    remaining_edges = set(graph.edge_weights.keys())
    while len(no_incoming) != 0:
        # select the next vertex for the final result.
        current_vertex = no_incoming.pop()
        result_list.append(current_vertex)
        outgoing_edges = []

        # remove current_vertex's outgoing edges from remaining_edges.
        for to_vertex in graph.adjacency_list[current_vertex]:
            outgoing_edge = (current_vertex, to_vertex)
            if outgoing_edge in remaining_edges:
                outgoing_edges.append(outgoing_edge)
                remaining_edges.remove(outgoing_edge)
        
        # see if removing the outgoing edges creates any new vertices
        # with no incoming edges.
        for (from_vertex, to_vertex) in outgoing_edges:
            in_count = get_incoming_edge_count(remaining_edges, to_vertex)
            if in_count == 0:
                no_incoming.append(to_vertex)
    
    return result_list

if __name__ == "__main__":
    # make a graph
    g = Graph()
    
    vertex_A = Vertex('A')
    vertex_B = Vertex('B')
    vertex_C = Vertex('C')
    vertex_D = Vertex('D')
    vertex_E = Vertex('E')
    vertex_F = Vertex('F')
    vertex_G = Vertex('G')
    
    g.add_vertex(vertex_A)
    g.add_vertex(vertex_B)
    g.add_vertex(vertex_C)
    g.add_vertex(vertex_D)
    g.add_vertex(vertex_E)
    g.add_vertex(vertex_F)
    g.add_vertex(vertex_G)

    g.add_directed_edge(vertex_A, vertex_B)
    g.add_directed_edge(vertex_A, vertex_C)
    g.add_directed_edge(vertex_B, vertex_F)
    g.add_directed_edge(vertex_C, vertex_D)
    g.add_directed_edge(vertex_D, vertex_F)
    g.add_directed_edge(vertex_E, vertex_F)
    g.add_directed_edge(vertex_E, vertex_G)
    g.add_directed_edge(vertex_F, vertex_G)
    
    # do topological sort on the graph
    result_list = topological_sort(g)
    
    # display sorted list
    first = True
    for vertex in result_list:
        if first:
            first = False
        else:
            print(' -> ', end='')
        print(vertex.label, end='')
    print()
