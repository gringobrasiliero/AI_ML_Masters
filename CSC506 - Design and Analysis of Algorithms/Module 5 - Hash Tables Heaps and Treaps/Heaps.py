
class MinHeap:
    def __init__(self):
        self.heap_array = []

    def percolate_up(self, node_index):
        while node_index > 0:
            # compute the parent node's index
            parent_index = (node_index - 1) // 2
        
            # check for a violation of the min heap property
            if self.heap_array[node_index] >= self.heap_array[parent_index]:
                # no violation, so percolate up is done.
                return
            else:
                # swap heap_array[node_index] and heap_array[parent_index]
                temp = self.heap_array[node_index]
                self.heap_array[node_index] = self.heap_array[parent_index]
                self.heap_array[parent_index] = temp
            
                # continue the loop from the parent node
                node_index = parent_index

    def percolate_down(self, node_index):
        child_index = 2 * node_index + 1
        value = self.heap_array[node_index]

        while child_index < len(self.heap_array):
            # Find the min among the node and the node's children
            min_value = value
            min_index = -1
            i = 0
            while i < 2 and i + child_index < len(self.heap_array):
                if self.heap_array[i + child_index] < min_value:
                    min_value = self.heap_array[i + child_index]
                    min_index = i + child_index
                i = i + 1

            # check for a violation of the min heap property
            if min_value == value:
                return
            else:
                # swap heap_array[node_index] and heap_array[min_index]
                temp = self.heap_array[node_index]
                self.heap_array[node_index] = self.heap_array[min_index]
                self.heap_array[min_index] = temp
            
                # continue loop from the larger child node
                node_index = min_index
                child_index = 2 * node_index + 1

    def insert(self, value):
        # add the new value to the end of the array.
        self.heap_array.append(value)
    
        # percolate up from the last index to restore heap property.
        self.percolate_up(len(self.heap_array) - 1)

    
    def remove(self):
        # save the min value from the root of the heap.
        min_value = self.heap_array[0]
    
        # move the last item in the array into index 0.
        replace_value = self.heap_array.pop()
        if len(self.heap_array) > 0:
            self.heap_array[0] = replace_value
        
            # percolate down to restore min heap property.
            self.percolate_down(0)
            
        # return the min value
        return min_value

list = [25, 44, 55, 99, 30, 37, 15, 10, 2, 4]
#list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
x = MinHeap()


for i in list:
    x.insert(i)

print(x.heap_array)