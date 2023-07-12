import numpy as np

class Helpers():
    def __init__(self):
        pass
    def convert_binary(self, image_matrix, thresh_val):
        w = 255
        b = 0
    
        initial = np.where((image_matrix <= thresh_val), image_matrix, w)
        final = np.where((initial > thresh_val), initial, b)
    
        return final

