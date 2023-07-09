#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random









def main():
    number_count = 1000000000
    with open('hugefile1.txt', 'w') as f:
        for i in range(number_count-1):
            random_int_line = str(random.randint(0,32767)) + "\n"
            f.write(random_int_line)
        random_int_line = str(random.randint(0,32767)) #No New Line on last number inserted
        f.write(random_int_line)
    pass





if __name__ == '__main__' : main()

