#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

class Customer_account():
    count = 0
    def __init__(self, name, initial_balance):
        self.name = name
        self.account_balance = initial_balance
        self.id = self.assign_id()
        self.closed = False
    
    @classmethod
    def assign_id(self):
        self.count += 1
        return self.count
        
    def withdraw_funds(self,amount):
        self.account_balance -= amount
        if self.account_balance == 0:
            self.closed = True

class Card():
    max_login_attempts = 3

    def __init__(self, pin, account_id):
        self.card_number = self.generate_card_number()
        self.pin = pin
        self.account_id = account_id
        self.failed_login_attempts = 0
        self.locked = self.failed_login_attempts == 3

    def increase_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts == self.max_login_attempts:
            self.locked = True
    
    def generate_card_number(self):
        card_number = ""
        for i in range(0,8):
            card_number += str(random.randint(0,9))
        return card_number


class Bank():
    def __init__(self):
        self.cards = []
        self.customer_accounts = []
    
    def create_customer_account_with_card(self, name, initial_balance, pin):
        customer = Customer_account(name, initial_balance)
        card = Card(pin, customer.id)
        self.customer_accounts.append(customer)
        self.cards.append(card)
        self.provide_account_details(customer,card)


    def provide_account_details(self, customer, card):
        print("****BANK ACCOUNT INFO****")
        print("Name: " + customer.name)
        print("Balance: $" + str(customer.account_balance))
        print("Card_number: " + card.card_number[0:4] + "-" + card.card_number[4:])
        print("PIN: " + card.pin)
        print("*************************\n\n\n")

    def verify_card_number(self, card_num):
        for card in self.cards:
            
            if card_num == card.card_number:
                if card.locked:
                    print("The Card is locked. Visit your local bank to get a new card.\n")
                    return False
                else:
                    #Verified Card Number
                    return True
        print("Invalid Card Number. Please Try Again.\n")
        return False

    def check_pin(self, card_number, pin):
        card = self.get_card_by_card_number(card_number)
        if card.pin == pin:
            customer_account = self.get_customer_account_by_id(card.account_id)
            return customer_account
        else:
            #Failed Login Attempt
            print("Invalid PIN.\n")
            card.increase_failed_login_attempts()
            return None        
        pass

    def get_card_by_card_number(self,card_number):
        for card in self.cards:
            if card.card_number == card_number:
                return card
        return None
    
    def get_customer_account_by_id(self,id):
        for account in self.customer_accounts:
            if account.id == id:
                return account
        return None



class ATM():
    def __init__(self, bank):
        self.current_customer = None
        self.bank = bank
        pass




    def authenticate(self):
        card_number = self.verify_card_number()
        self.insert_pin(card_number)
        
        pass

    def verify_card_number(self):
        verified_card_number = False
        while verified_card_number == False:
            card_num = input("Insert Card Number:\n")
            card_num = card_num.replace("-","")
            verified_card_number = self.bank.verify_card_number(card_num)

                
        return card_num

    def insert_pin(self, card_number):
        pin = input("Insert PIN:\n")
        customer = self.bank.check_pin(card_number, pin)
        if customer != None:
            if customer.closed:
                print("This account is no longer valid as it has been closed. Have a nice day...\n")
            else:
                self.current_customer = customer

    def print_account_details(self):
        print("\nBalance: $" + str(self.current_customer.account_balance) + "\n")

    def withdraw_funds(self):
        withdraw_amount = int(input("Amount to Withdraw:\n"))
        if withdraw_amount <= self.current_customer.account_balance:
            self.current_customer.withdraw_funds(withdraw_amount)
            print("Withdrawing $" + str(withdraw_amount) + ".\nNew Current Balance: $" + str(self.current_customer.account_balance) + "\n")
        else:
            print("Insufficent Funds.\n")

    def deposit_funds(self):
        deposit_amount = input("Deposit Amount:\n")
        self.current_customer.account_balance += int(deposit_amount)
        print("$" + str(deposit_amount) + " has been inserted into your account.\n Your current balance is: $" + str(self.current_customer.account_balance))



    def account_menu(self):
        while True:
            print("\n1. Check Balance\n2. Withdraw\n3. Deposit\n4. Log Out")
            menu_option = input()
            if menu_option == "1":
                self.print_account_details()
                pass
            elif menu_option == "2":
                self.withdraw_funds()
                if self.current_customer.closed:
                    print("The Account has been closed. Thank you for banking with us, and have a nice day.\n")
                    self.current_customer = None
                    break
                pass
            elif menu_option == "3":
                self.deposit_funds()
                break
            elif menu_option == "4":
                print("Have a nice day...")
                self.current_customer = None
                break
            else:
                print("Invalid Selection")

    def run(self):
        print("*************ATM*************")
        while True:
            if self.current_customer == None:
                selection = input("1. Log in\n2. Shut Down\n")
                if selection == "1":
                    self.authenticate()
                elif selection == "2":
                    break
                else:
                    print("Invalid Selection\n")
            else:
                self.account_menu()
        pass

def main():
    

    #Generates the Bank, and creates a default Customer Account with Linked Card.
    #This is so that there are Customer Accounts when beginning the program.

    #First Account created
    bank = Bank()
    name = "Mr. Moneybags"
    initial_balance = 1000000
    pin = "1234"
    bank.create_customer_account_with_card(name, initial_balance, pin)

    #Second Account created to test out getting a Card Blocked.
    name = "Forgetful Fran"
    initial_balance = 1
    pin = "9876"
    bank.create_customer_account_with_card(name, initial_balance, pin)

    atm = ATM(bank)
    atm.run()




    pass

if __name__ == '__main__' : main()