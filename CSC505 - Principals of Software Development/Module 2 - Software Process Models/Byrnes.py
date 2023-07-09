#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Byrnes(object):
    def __init__(self):
        self.current_phase_num = 0
        self.phases = ["Communication", "Planning", "Modeling Prototypes", "Prototyping", "Stakeholder Feedback", "Modeling", "Construction", "Deployment"]
        self.phase_description = {}
        self.phase_description["Communication"] = ["Project Initiation", "Requirements Gathering"]
        self.phase_description["Planning"] = ["Estimating", "Scheduling", "Tracking"]
        self.phase_description["Modeling Prototypes"] = ["Analysis", "Quick Designs"]
        self.phase_description["Prototyping"] = ["Code"]
        self.phase_description["Stakeholder Feedback"] = ["Demonstrate Prototypes to Stakeholders", "Receive Feedback on Prototypes", "Identify the best prototype for the final solution"]
        self.phase_description["Modeling"] = ["Analysis", "Design"]
        self.phase_description["Construction"] = ["Code", "Test"]
        self.phase_description["Deployment"] = ["Delivery", "Support", "Feedback"]

        self.phase_comments = {}
        pass
     

    def __print_phase(self, phase):
        phase_name = phase
        print("\nPhase: " + phase_name + "\n")

        phase_tasks = self.phase_description[phase_name]
        i=1
        for task in phase_tasks:
            print("   " + str(i) + ". " + task)
            i+=1

    def __print_comments(self, phase):
        phase_name = phase
        print("\n*******COMMENTS***\n")

        phase_comments = self.phase_comments[phase]

        i=1
        for comment in phase_comments:
            print("        " + str(i) + ". " + comment)
            i+=1
        print("******************")

    def nav_through_phases(self):
        welcome_statement = "Welcome to the Byrnes Model.\n"
        print(welcome_statement)
        phase_count = len(self.phases)
        while True:
            self.__print_phase(self.phases[self.current_phase_num])

            self.__get_comments_on_phase()
            self.current_phase_num = self.current_phase_num + 1

            if self.current_phase_num >= phase_count:
                print("\nYou have reached the end of the Byrnes Model, and your project should be completed.")
                break

    def __get_comments_on_phase(self):
        current_phase = self.phases[self.current_phase_num]
        
        request_comments_text = "\nPlease enter your Comments on the " + current_phase.upper() + " Phase before we proceed.\n"
        
        print(request_comments_text)
        comments = []

        while True:
            comment = input("\nType in your comment or press 'N' to Proceed:\n\t")
            if comment.upper() == "N":
                break
            else:
                comments.append(comment)

        self.phase_comments[current_phase] = comments
        pass
    
    def display_project_summary(self):
        print("\n***PROJECT SUMMARY***\n\n")
        for phase in self.phases:
            self.__print_phase(phase)
            self.__print_comments(phase)
            



def main():
    x = Byrnes()
    x.nav_through_phases()
    x.display_project_summary()

if __name__ == '__main__' : main()