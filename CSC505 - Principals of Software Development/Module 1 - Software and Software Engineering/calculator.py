#!/usr/bin/env python
# -*- coding: utf-8 -*-


def split_calculation(calc):
    calc = calc.replace(" ","")
    calc = calc.replace("+"," + ")
    calc = calc.replace("-"," - ")
    calc = calc.replace("/"," / ")
    calc = calc.replace("*"," * ")
    results = calc.split(" ")
    return results

def main():
    print("***CALCULATOR***\n Type in the Math problem that needs to be solved. Type in 'Exit' to Exit\n")
    while True:
        calc = input("What math problem do you need me to compute?\n")
        if calc.lower() == "exit":
            print("Exiting Calculator")
            break
        split_calc = split_calculation(calc)
        i = 0
        while i < len(split_calc):
            
            if i > 1:
                operator = split_calc[i]
                num_one = result
                num_two = float(split_calc[i+1])
            else:
                num_one = float(split_calc[i])
                num_two = float(split_calc[i+2])
                operator = split_calc[i+1]
            if operator == "+":
                result = num_one + num_two
            elif operator == "-":
                result = num_one - num_two
            elif operator == "/":
                result = num_one / num_two
            elif operator == "*":
                result = num_one * num_two
            i = i + 3 
        print(str(result))
        

if __name__ == '__main__' : main()