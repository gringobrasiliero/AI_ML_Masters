#!/usr/bin/env python
# -*- coding: utf-8 -*-

def findNext(digit_string):
    digits = list(map(int ,digit_string))
     # Identify the first digit starting from the end of the digit string where the digit to the left is greater than the digit on the right
    i = len(digit_string)-1
    while i > 0:
        left_num = digits[i-1]
        right_num = digits[i]
        if left_num < right_num:
             # Split the string in two, so that the right part is in decreasing order
            left_digit_split = digits[:i]
            right_digit_split = digits[i:]
            break
        i-=1
    # If all digits are in descending order, there is not a higher number
    if i == 0 and left_num > right_num:
        return False, []

    # Find the smallest number in the right sequence that is larger than the last_digit_of_left.
    j = 0
    smallest = j
    j+=1
    while j <= len(right_digit_split)-1:
        current_num = right_digit_split[j]
        if current_num > left_num and current_num < right_digit_split[smallest]:
            smallest = j
        j+=1

    #Swap the last digit from the Left sequence with the smallest number of right sequence that is greater than left
    left_digit_split[-1] = right_digit_split[smallest]
    right_digit_split[smallest]= left_num
    # Sort the right sequence
    right_digit_split.sort()
    # Combine the left and right sequence together
    combined_digits = left_digit_split + right_digit_split
    #Convert back to Digit String
    next_digit_string =  str("".join(map(str,combined_digits)))
 
    return True, next_digit_string
    
def main():
    digit_string = "123"
    had_higher_number, digit_string = findNext(digit_string)
    if had_higher_number:
        print("The next highest number is " + digit_string + ".")
    else:
        print("There is not a higher number available.")
    pass

if __name__ == '__main__' : main()


    
   