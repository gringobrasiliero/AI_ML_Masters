
# coding=utf-8
from simpleai.search import astar, greedy, uniform_cost, SearchProblem
from simpleai.search.viewers import WebViewer


GOAL = '1 2 3\n4 5 _'

INITIAL = '2 1 _\n4 5 3'

def construct_puzzle():
    print("Give me an 8-puzzle to solve. Enter the values that should be in the 3x3 square, with one space being an underscore to represent the empty slot.\n")
    i=0
    rows = []
    while i < 3:
        row_string = input("What 3 characters should be on row " + str(i)+"\n")
        input_len = len(row_string)
        if input_len != 3:
            print("Please only input 3 characters")
        else:
            rows.append(row_string)
            i+=1
    rows = list_to_string(rows)
    print("The initial puzzle will look like this:\n")
    print(rows)

    return rows




def construct_final_puzzle(initial_puzzle):
    chars_left = flatten_puzzle(string_to_list(initial_puzzle))
    print("\nConstruct what the final puzzle should be\n")
    i=0
    rows = []
    while i < 3:
        row_string = input("What 3 characters should be on row " + str(i) + "?\n\tChars Left: " + str(chars_left)+"\n")
        input_len = len(row_string)
        if input_len != 3:
            print("Please only input 3 characters")
        else:
            row = row_string.split()
            for c in row_string:
                chars_left.remove(c)
            rows.append(row_string)
            i+=1
    final_puzzle = list_to_string(rows)
    print("This is what the puzzle will look like after I solve it:\n")
    print(final_puzzle)
    return final_puzzle


def flatten_puzzle(puzzle):
    chars_used = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            current_char = puzzle[i][j]
            chars_used.append(current_char)
    return chars_used

def list_to_string(list_):
    return '\n'.join([' '.join(row) for row in list_])

def string_to_list(string_):
    return [row.split(' ') for row in string_.split('\n')]

def find_location(rows, desired_element):
    for r in range(len(rows)):
        for c in range(len(rows[r])):
            curr_element = rows[r][c]
            if curr_element == desired_element:
                x = r, c
                return r, c


def print_grid(positions):
    grid = positions[0][0] + " " + positions[0][1] + " " + positions[0][2] + "\n" + positions[1][0] + " " + positions[1][1] + " " + positions[1][2] + "\n" + positions[2][0] + " " + positions[2][1] + " " + positions[2][2]
    return grid


class EightPuzzleProblem(SearchProblem):
    def actions(self, rows):
        rows = string_to_list(rows)
        possible_actions = []
        empty_row,empty_column = find_location(rows,"_")
        if empty_row > 0:
            possible_actions.append(rows[empty_row-1][empty_column])
        if empty_row < 2:
            possible_actions.append(rows[empty_row+1][empty_column])
        if empty_column > 0:
            possible_actions.append(rows[empty_row][empty_column-1])
        if empty_column < 2:
            possible_actions.append(rows[empty_row][empty_column+1])
        return possible_actions


    def cost(self, state1, action, state2):
        return 1


    def result(self, rows, action):
        rows = string_to_list(rows)
        empty_row,empty_column = find_location(rows,"_")
        target_row,target_column = find_location(rows,action)
        rows[empty_row][empty_column], rows[target_row][target_column] = rows[target_row][target_column], rows[empty_row][empty_column]
        return list_to_string(rows)
      



    def is_goal(self, state):

        return state == GOAL

    def heuristic(self, state):
        # Gives us how far away from the goal we are
        rows = state
        distance = 0
        row_len = len(state)
        for r in range(row_len):
            col_len = len(state[r])
            for c in range(col_len):
                current_cell = state[r][c]
                row_goal, column_goal = find_location(GOAL,current_cell)

                distance += abs(r - row_goal) + abs(c - column_goal)
        return distance


INITIAL = construct_puzzle()
GOAL = construct_final_puzzle(INITIAL)

def main():
    
    
    
    problem = EightPuzzleProblem(INITIAL)

    result = astar(problem)
    print("\n\nI was able to solve the puzzle in " + str(len(result.path())-1) + " Moves. Below are the steps I made to solve the puzzle.\n")
    i=0
    for action, state in result.path():
        print("Step #"+str(i))
        print('Moved number ' + str(action) + "\n")
        print(state)
        print("\n")
        i+=1
if __name__ == "__main__":
    main()



