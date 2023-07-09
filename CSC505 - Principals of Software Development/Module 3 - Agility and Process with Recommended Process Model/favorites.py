#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

class FavoriteApps(object):
    
    def __init__(self):
        self.categorized_apps = {}
        self.categorized_apps["Productivity"] = ["Evernote", "Calculator"]
        self.categorized_apps["Games"] = ["Candy Crush", "Poker"]
        self.categorized_apps["Social Media"] = ["LinkedIn"]
        #self.categorized_apps["Education"] = ["Canvas", "Duolingo"]

        self.main_menu_text = "\n\n1. Select Category\n2. Add Category\n3. Remove Category\n4. Exit\n"
        self.category_menu_text = "\n\n1. Open Application\n2. Add Application\n3. Remove Application\n4. Main Menu\n"
        pass


    def print_categories(self):
        for category in self.categorized_apps:
            print(category)

    def print_applications(self, category):
        print("\n*****" + category + "*****")
        for app in self.categorized_apps[category]:
            print(app)


    def select_category(self):
        category = input("What Category would you like to view?\n")
        if category in self.categorized_apps:
            self.category_screen(category)
        else:
            selection = input("The " + category + " category does not exist. Would you like to add it as a new category instead?\n(Select 'Y' to include the new category)\n" )
            if selection == "Y":
                self.add_category(category)
    
    def select_application(self, category):
        app = input("Which Application would you like to open?\n")
        if app in self.categorized_apps[category]:
            self.load_application()
        pass


    def add_category(self, category):
        if not category in self.categorized_apps:
            self.categorized_apps[category] = []
        else: 
            print("The " + category + " category already exists.\n")

    def add_application(self, category):
        app = input("Which Application would you like to include?\n")
        if not app in self.categorized_apps[category]:
            self.categorized_apps[category].append(app)
        else:
            print(app + " Application has already been added.\n")

    def remove_application(self, category):
        app_to_remove = input("Which Application would you like to remove?\n")
        index = 0
        if app_to_remove in self.categorized_apps[category]:
            while index < len(self.categorized_apps[category]):
                if app_to_remove == self.categorized_apps[category][index]:
                    self.categorized_apps[category].pop(index)
                    break
                else:
                    index += 1

    def remove_category(self, category):
        if category in self.categorized_apps:
            self.categorized_apps.pop(category)
        else:
            print("Category does not exist.\n")
        pass

    def main_menu_screen(self):
        while True:
            print("\n*****MAIN MENU*****\n")
            self.print_categories()
            print(self.main_menu_text)
            selection = input("")
            if selection == "1":
                self.select_category()
                pass
            elif selection == "2":
                category = input("What Category would you like to add?\n")
                self.add_category(category)
                pass
            elif selection == "3":
                category = input("What Category would you like to remove?\n")
                self.remove_category(category)
                pass
            elif selection == "4":
                break

    def category_screen(self, category):
        while True:
            self.print_applications(category)
            print(self.category_menu_text)
            selection = input()
            if selection == "1":
                self.select_application(category)
                pass
            elif selection == "2":
                self.add_application(category)
                pass
            elif selection == "3":
                self.remove_application(category)
            elif selection == "4":
                break

    def load_application(self):
        dots = ""
        for i in range(10):
            if i % 2 == 0:
                dots = "..."
            else:
                dots = ".. "
            print("Loading" + dots, end="\r")
            time.sleep(.5)
        print("\n")
        pass

def main():
    favoriteApps = FavoriteApps()
    favoriteApps.main_menu_screen()
    
    

if __name__ == '__main__' : main()