
class EdgeWeight:
    def __init__(self, from_vertex, to_vertex, weight):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight
    
    # Only edge weights are used in the comparisons that follow
    
    def __eq__(self, other):
        return self.weight == other.weight
    
    def __ge__(self, other):
        return self.weight >= other.weight
    
    def __gt__(self, other):
        return self.weight > other.weight

    def __le__(self, other):
        return self.weight <= other.weight
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __ne__(self, other):
        return self.weight != other.weight
