
def display_matrix(matrix):
    # This function assumes a simple matrix, where each entry is either an 
    # integer in the range [-99, 99], or infinity.
    
    for row in matrix:
        print("[ ", end="")
        for entry in row:
            # Case 1: entry is infinity
            if entry == float("inf"):
                print("inf", end=" ")

            # Case 2: entry is negative
            elif entry < 0:
                # Case 2A: entry is > -10
                if entry > -10:
                    print(str(entry), end="  ")
                # Case 2B: entry is <= -10
                else:
                    print(str(entry), end=" ")


            # Case 3: entry is non-negative
            else:
                # Case 3A: entry is < 10
                if entry < 10:
                    print(" " + str(entry) + " ", end=" ")
                # Case 3B: entry is >= 10
                else:
                    print(" " + str(entry), end=" ")
        print("]")
