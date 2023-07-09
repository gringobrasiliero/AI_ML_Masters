
from graph import Vertex, Graph
from EdgeWeight import EdgeWeight
from VertexSetCollection import VertexSetCollection
import heapq

# Returns a list of edges representing the graph's minimum spanning tree.
# Uses Kruskal's minimum spanning tree algorithm.
def minimum_spanning_tree(graph):
    # edge_list starts as a list of all edges from the graph
    edge_list = []
    for edge in graph.edge_weights:
        edge_weight = EdgeWeight(edge[0], edge[1], graph.edge_weights[edge])
        edge_list.append(edge_weight)
    # Turn edge_list into a priority queue (min heap)
    heapq.heapify(edge_list)

    # Initialize the collection of vertex sets
    vertex_sets = VertexSetCollection(graph.adjacency_list)

    # result_list is initially an empty list
    result_list = []

    while len(vertex_sets) > 1 and len(edge_list) > 0:
        # Remove edge with minimum weight from edge_list
        next_edge = heapq.heappop(edge_list)
        
        # set1 = set in vertex_sets containing next_edge's 'from' vertex
        set1 = vertex_sets.get_set(next_edge.from_vertex)
        # set2 = set in vertex_sets containing next_edge's 'to' vertex
        set2 = vertex_sets.get_set(next_edge.to_vertex)
        
        # If the 2 sets are distinct, then merge
        if set1 is not set2:
            # Add next_edge to result_list
            result_list.append(next_edge)
            # Merge the two sets within the collection
            vertex_sets.merge(set1, set2)

    return result_list


# Main program 1
graph1 = Graph()

# Add vertices A through H
vertex_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
for vertex_name in vertex_names:
    graph1.add_vertex(Vertex(vertex_name))

# Add edges
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("B"), 15)
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("D"), 6)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("C"), 9)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("D"), 12)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("G"), 14)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("H"), 10)
graph1.add_undirected_edge(graph1.get_vertex("C"), graph1.get_vertex("E"), 16)
graph1.add_undirected_edge(graph1.get_vertex("D"), graph1.get_vertex("E"), 8)
graph1.add_undirected_edge(graph1.get_vertex("E"), graph1.get_vertex("F"), 20)

# Get the list of edges for the graph's minimum spanning tree
tree_edges = minimum_spanning_tree(graph1)

# Display the list of edges
print("Edges in minimum spanning tree (graph 1):")
for edge in tree_edges:
    print(edge.from_vertex.label + " to " + edge.to_vertex.label, end="")
    print(", weight = " + str(edge.weight))

# Main program 2
graph2 = Graph()

# Add vertices A through G, and P
vertex_names = ["A", "B", "C", "D", "E", "F", "G", "P"]
for vertex_name in vertex_names:
    graph2.add_vertex(Vertex(vertex_name))

# Add edges
graph2.add_undirected_edge(graph2.get_vertex("A"), graph2.get_vertex("B"), 80)
graph2.add_undirected_edge(graph2.get_vertex("A"), graph2.get_vertex("C"), 105)
graph2.add_undirected_edge(graph2.get_vertex("A"), graph2.get_vertex("E"), 182)
graph2.add_undirected_edge(graph2.get_vertex("B"), graph2.get_vertex("C"), 90)
graph2.add_undirected_edge(graph2.get_vertex("B"), graph2.get_vertex("D"), 60)
graph2.add_undirected_edge(graph2.get_vertex("B"), graph2.get_vertex("P"), 100)
graph2.add_undirected_edge(graph2.get_vertex("C"), graph2.get_vertex("P"), 132)
graph2.add_undirected_edge(graph2.get_vertex("D"), graph2.get_vertex("E"), 80)
graph2.add_undirected_edge(graph2.get_vertex("E"), graph2.get_vertex("F"), 70)
graph2.add_undirected_edge(graph2.get_vertex("F"), graph2.get_vertex("G"), 72)
graph2.add_undirected_edge(graph2.get_vertex("F"), graph2.get_vertex("P"), 145)
graph2.add_undirected_edge(graph2.get_vertex("G"), graph2.get_vertex("P"), 180)

# Get the list of edges for the graph's minimum spanning tree
tree_edges = minimum_spanning_tree(graph2)

# Display the list of edges
print("Edges in minimum spanning tree (graph 2):")
for edge in tree_edges:
    print(edge.from_vertex.label + " to " + edge.to_vertex.label, end="")
    print(", weight = " + str(edge.weight))
