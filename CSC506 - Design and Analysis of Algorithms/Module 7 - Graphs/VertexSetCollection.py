
class VertexSetCollection:
    def __init__(self, all_vertices):
        self.vertex_map = dict()
        for vertex in all_vertices:
            vertex_set = set()
            vertex_set.add(vertex)
            self.vertex_map[vertex] = vertex_set

    def __len__(self):
        return len(self.vertex_map)

    # Gets the set containing the specified vertex
    def get_set(self, vertex):
        return self.vertex_map[vertex]

    # Merges two vertex sets into one
    def merge(self, vertex_set1, vertex_set2):
        # First create the union
        merged = vertex_set1.union(vertex_set2)
        # Now remap all vertices in the merged set
        for vertex in merged:
            self.vertex_map[vertex] = merged
