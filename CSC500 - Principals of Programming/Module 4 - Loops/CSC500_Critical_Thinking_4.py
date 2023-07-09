#!/usr/bin/env python3

import calendar

def main():

    num_of_years = ask_for_number("int", "How many years of rainfall data do you have?\n")
    year = 1    
    months_in_year = 12
    total_inches_of_rainfall = 0
    
    while year <= num_of_years:
        month = 1 
        while month <= months_in_year:
            cmd_text = "How much rain occurred in " + calendar.month_name[month] + " of year " + str(year) + "?\n"
            inches_of_rainfall = ask_for_number("float", cmd_text)
            total_inches_of_rainfall += inches_of_rainfall 
            month += 1
        year += 1

    total_months = num_of_years * months_in_year
    average_rainfall = total_inches_of_rainfall / total_months 
    print("The total number of months of rainfall data provided is", total_months)
    print("The total inches of rainfall is", round(total_inches_of_rainfall, 2))
    print("The average amount of rainfall per month is", round(average_rainfall, 2))
    pass


def ask_for_number(number_type, text):
    not_number = True
    while not_number: 
        res = input(text)
        try:
            if number_type == "int":
                return int(res)
            elif number_type == "float":
                return float(res)        
        except ValueError:
            not_number = True
            if number_type == "int":
                print("Please provide an integer as your response.\n")
            elif number_type == "float":
                print("Please provide a float as your response.\n")        
            


if __name__ == '__main__' : main()