#!/usr/bin/env python
# -*- coding: utf-8 -*-

def daily_salary_loop(first_day_salary, total_days):
    daily_salary = first_day_salary
    print("Day 1 Salary: " + str(first_day_salary))
    for day in range(2, total_days+1):
        daily_salary = round(daily_salary * 2, 2)
        print("Day " + str(day) + " Salary: " + str(daily_salary))
    pass

def main():
    daily_salary_loop(.01, 30)
    pass

if __name__ == '__main__' : main()

