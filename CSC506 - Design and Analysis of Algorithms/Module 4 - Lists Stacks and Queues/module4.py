#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Queue():
    def __init__(self):
        self.inbox = []
        self.outbox = []
        pass

    def push(self, value):
        self.inbox.append(value)

    def dequeue(self):
        if len(self.outbox)==0 and len(self.inbox)!=0:
            while len(self.inbox) != 0:
                self.outbox.append(self.inbox.pop())
            return self.outbox.pop()
        elif len(self.outbox) != 0:
            return self.outbox.pop()
        else:
            return
def main():    
    x = Queue()
    x.dequeue()

    for i in range(1,5,1):
        print(i)
        x.push(i)
    
    o = x.dequeue()
    print("The Item removed from the Queue is: " + str(o))
    
    print("The Items remaining in the Queue are: " + str(x.outbox))
    pass

if __name__ == '__main__' : main()





