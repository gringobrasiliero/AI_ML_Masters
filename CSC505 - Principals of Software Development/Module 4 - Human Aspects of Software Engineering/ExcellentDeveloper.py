#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc

class Excellent_developer():
    
    def __init__(self, name):
        self.personality = None
        self.name = name
        self.greeting = "Hello, my name is " + self.name + " , and I was developed by Nolan Byrnes to be an example of an Excellent Software Developer.\nI do have a personality, and as of this first release I have the following personality traits that I can use:\n\t1. Eagerness to learn\n\t2. Empathy\n\t3. Fairness\n\nDepending on how you communicate with me, I will be able to respond by using my different personality traits.\n"
        self.fairwell_message = "Goodbye. It was nice chatting with you."
        pass

    def set_personality(self, personality):
        self.personality = personality
        pass

    def say_greetings(self):
        print(self.greeting)
        pass

    def have_conversation(self):
        selection_options = "\nWhat would you like to discuss?\n\n1. Talk about Python\n2. Tell me a new project idea\n3. Give me a compliment\n4. End Conversation\n\n"
        while True:
            selection = input(selection_options)
            if selection == "1":
                personality_trait = Eagerness_to_learn()
                pass
            elif selection == "2":
                personality_trait = Empathy()
                pass
            elif selection == "3":
                personality_trait = Fairness()
                pass
            elif selection == "4":
                break
            else:
                print("Invalid Selection. Please select '1', '2', '3', or '4'.\n")
                continue

            self.set_personality(personality_trait)
            self.personality.talk_with_personality()
    
    
    def say_fairwell(self):
        print(self.fairwell_message)
        pass
    
    pass

class IPersonality(abc.ABC) :
    @abc.abstractclassmethod
    def talk_with_personality():
        pass

class Eagerness_to_learn(IPersonality) :
    def talk_with_personality(self):
        print("\nI have an eagerness to learn. What can you tell me about developing in Python?\n")
        while True:
            facts = input("")
            if facts == "no":
                break
            else:
                print("Interesting. Thank you. Can you tell me more? If not, just tell me 'no'.")
        pass
    pass

class Empathy(IPersonality):
    def talk_with_personality(self):
        idea = input("\nWhat do you think would be a great application to develop is?\n")
        end_users = input("Who would the end users be?")
        print("\nI like where you are going with this...\nLet me think about how " + end_users + " would use an application like this, and I will schedule a meeting for next week and discuss our next steps.")
        pass

class Fairness(IPersonality):
    def talk_with_personality(self):
        compliment = input("\nOh? What is the compliment?\n")
        print("\nThank you for the compliment, however, this could not have happened without my creator, Nolan Byrnes, or his Professor Steven Evans.")
        pass

def main():
    dev = Excellent_developer("Mr. Roboto")
    dev.say_greetings()
    dev.have_conversation()
    dev.say_fairwell()
    pass

if __name__ == '__main__' : main()


