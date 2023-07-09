#!/usr/bin/env python
# -*- coding: utf-8 -*-

def daily_salary_recursion(daily_salary, day, total_days):
    if day <= total_days: #Base Case
        if day != 1:
            daily_salary = round(daily_salary * 2, 2)
        print("Day " + str(day) + " Salary: " + str(daily_salary))
        day +=1
        daily_salary_recursion(daily_salary, day, total_days) #Recursive Call
    pass

def main():    
    daily_salary_recursion(.01, 1, 30)
    pass

if __name__ == '__main__' : main()

