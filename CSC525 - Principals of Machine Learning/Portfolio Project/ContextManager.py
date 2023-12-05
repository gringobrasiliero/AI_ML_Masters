
import json
import pandas as pd
from cleaners import clean_data
import re

class ContextManager():
    #This class helps manage the Context of conversations, keeping the context to stay under the max length of tokens. (Default is 100)
    def __init__(self):
        self.max_length = 100
        self.context = []
        self.word_count = 0
        self.user_token = "<user>"
        self.system_token = "<system>"
        pass

    def insert_context(self, words):
        #Cleaning Text
        words=clean_data(words)
        #Getting list of words with max len limit
        words = list(words.split(" "))[:self.max_length]
        #Add the words to the context
        self.context.append(words)
        #Increase the word count
        self.word_count += len(words)
        #If the word count is above the limit, pop the first index of the list until it is under the word limit.
        while self.word_count >= self.max_length:
            words_popped = len(self.context[0])
            self.context.pop(0)
            self.word_count -= words_popped  
        pass

    def get_context(self):
        #Grab all of the current context
        context = [word for statement in self.context for word in statement]
        #Convert the flattened list into a string.
        context = " ".join(map(str,context))
        return context

    def clear_context(self):
        self.context = []
        self.word_count = 0
