#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Citizen():
    count = 0

    def __init__(self, name, address, phone_number):
        self.id = self.assign_id()
        self.name = name
        self.address = address
        self.phone_number = phone_number
        pass

    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count

class Pothole():
    count = 0

    def __init__(self, citizen_id, address, size, location):
        self.id = self.assign_id()
        self.citizen_id = citizen_id
        self.street_address = address
        self.location = location
        self.size = size
        self.district = self.determine_district(address)
        self.repair_priority = self.determine_repair_priority(size)
        pass
        
    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count

    def determine_district(self, street_address):
        district = ""
        street_address.strip()
        street_address_split = street_address.split()
        house_number = street_address_split[0]

        if house_number.isnumeric():
            if int(house_number) <=2500:
                district = "1"
            elif int(house_number) <=5000:
                district = "2"
            elif int(house_number) <=7500:
                district = "3"
            elif int(house_number) <=5000:
                district = "4"
        else:
            district = 0

        return district

    def determine_repair_priority(self, size):
        repair_priority = ""
        if size <= 3:
            repair_priority = "Low"
        elif size <= 6:
            repair_priority = "Medium"
        elif size <= 10:
            repair_priority = "High"
        return repair_priority

class Work_order():
    count = 0

    def __init__(self, pothole, repair_crew):
        self.id = self.assign_id()
        self.pothole_id = pothole.id
        self.citizen_id = pothole.citizen_id
        self.pothole_location = pothole.location
        self.pothole_size = pothole.size
        self.repair_crew_id = repair_crew.id
        self.crew_size = repair_crew.crew_size
        self.equipment_assigned = self.assign_equipment(pothole.repair_priority)
        self.type_of_damage = ""
        self.hours_applied = 0
        self.status = "work in progress"
        self.amount_of_filler_material = 0
        self.cost_of_repair = 0

        pass

    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count

    def assign_equipment(self, repair_priority):
        if repair_priority == "Low":
            equipment = "Shovel, Small Truck"
        elif repair_priority == "Medium":
            equipment = "Shovel, Wheelbarrow, Medium Truck"
        elif repair_priority == "High":
            equipment = "Shovel, Wheelbarrow, Large Truck"
        else:
            equipment = ""
        return equipment

    def update_work_order(self, hourly_rate):
       hours_applied= input("\nHours to Add: ")
       while True:
           status = input("\nStatus (work in progress, repaired, temporary repair, not repaired):\n")
           if status in ["work in progress", "repaired", "temporary repair", "not repaired"]:
               break
           else:
               print("\nPlease select a valid status (work in progress, repaired, temporary repair, not repaired)")

       filler_material = input("\nFiller Material Used (Pounds) : ")
       if hours_applied != "":
           hours = self.hours_applied + int(hours_applied)
           self.hours_applied = hours
       if status != "":
           self.status = status
       if filler_material != "":
           self.amount_of_filler_material = int(filler_material)


       type_of_damage = input("Type of Damage: ")
       self.type_of_damage = type_of_damage

       labor_cost = self.hours_applied * hourly_rate
       #Filler Material is sold in 50 pound bags and sold at 20 dollars per 50 pounds
       parts_cost = (self.amount_of_filler_material/50) * 20

       self.cost_of_repair = labor_cost + parts_cost

       pass
    
    def print_work_order(self):
         print("Pothole Location: " + self.pothole_location)
         print("Pothole Size: " + str(self.pothole_size))
         print("Equipment Assigned: " + self.equipment_assigned)
         print("Hours Worked: " + str(self.hours_applied))
         print("Amount of Filler Material Used: " + str(self.amount_of_filler_material))
         print("Cost of Repair: " + str(self.cost_of_repair))
         print("Work Order Status: " + self.status )

class Repair_crew():
    count = 0

    def __init__(self, name, size, hourly_rate):
        self.id = self.assign_id()
        self.name = name
        self.crew_size = size
        self.hourly_rate = hourly_rate
        pass

    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count

class Damage_file():
    def __init__(self, citizen_name, citizen_address, citizen_phone_number, type_of_damage, dollar_amount_of_damage):
        self.citizen_name = citizen_name
        self.citizen_address = citizen_address
        self.citizen_phone_number = citizen_phone_number
        self.type_of_damage = type_of_damage
        self.dollar_amount_of_damage = dollar_amount_of_damage

    def print_damage_file_summary(self):
        print("\n*****DAMAGE FILE SUMMARY*****")
        print("Citizen Name: " + self.citizen_name)
        print("Citizen Address: " + self.citizen_address)
        print("Citizen Phone Number: " + self.citizen_phone_number)
        print("Type of Damage: " + self.type_of_damage)
        print("Dollar Amount of Damage: " + str(self.dollar_amount_of_damage))

class PHTRS():
    
    def __init__(self):
        self.greeting = "Welcome to the Pothole Tracking and Repair System. Please log in or Create an account to continue.\n"
        self.login_menu = "\n1. Create an Account\n2. Log In\n3. Exit\n"
        self.citizens = []
        #repair_crews to be sorted by Crew Size in ascending order each time new repair crew is added
        self.repair_crews = [Repair_crew("Small Team", 3, 100),Repair_crew("Medium Team", 6, 200),Repair_crew("Large Team", 9, 300)]
        self.potholes = []
        self.work_orders = []
        self.damage_files = []
        self.current_user = None
        price_of_filler_material = 20

        pass

    def main_menu(self):
        print("*****MAIN MENU*****")
        print(self.greeting)
        
        while True:
            menu_selection = input(self.login_menu)
            if menu_selection == "1":
                self.create_account()
            elif menu_selection == "2":
                account_type = input("\nSelect 1 to log in as Citizen or 2 for Repair Crew?\n\n1. Citizen\n2. Repair Crew\n")
                if account_type == "1":
                    citizen = self.login_citizen()
                    if self.current_user != None:
                        self.citizen_menu()
                    else:
                        print("\nLogin Failed. Returning to Login Menu.\n")
                    
                elif account_type == "2":
                    self.login_repair_crew()
                    if self.current_user != None:
                        self.repair_crew_menu()
                    else:
                        print("\nLogin Failed. Returning to Login Menu.\n")
            elif menu_selection == "3":
                break
            else:
                print("Invalid Selection\n")
        pass



    def citizen_menu(self):
        while True:
            menu_selection = input("\n1. Report New Pothole\n2. Log Out\n")
            if menu_selection == "1":
                pothole = self.report_pothole()
                repair_crew = self.assign_repair_crew(pothole.repair_priority)
                work_order = Work_order(pothole, repair_crew)
                self.work_orders.append(work_order)
                print("\nThank you for your submission. A work order has been created, and a Repair Crew has been assigned.\n\n****Pothole Summary***")
                self.print_created_work_order(work_order, repair_crew)

            elif menu_selection == "2":
                self.current_citizen = None
                print("\nLogging Out.\n")
                break
            else:
                print("Invalid Selection\n")

        pass

    def repair_crew_menu(self):
        while True:
            assigned_work_orders = self.get_assigned_work_orders(self.current_user.id)
            self.print_assigned_work_orders(assigned_work_orders)
            menu_selection = input("\n\nSelect the ID of the Work Order to view the details or select 'exit' to Log Out\n")
            if menu_selection.isnumeric():
                work_order = self.get_by_id(int(menu_selection), self.work_orders)
                if work_order != None:
                    self.work_order_menu(work_order)
                    pass
            elif menu_selection == "exit":
                break
            else:
                print("Invalid Selection\n")
        pass

    def work_order_menu(self, work_order):
        while True:
            print("\n*****WORK ORDER SUMMARY*****\n")
            work_order.print_work_order()
            menu_selection = input("\n\n1. Update Work Order\n2. Complete Work Order\n3. Exit\n")

            if menu_selection == "1":
                work_order.update_work_order(self.current_user.hourly_rate)
                pass
            elif menu_selection == "2":
                if work_order.amount_of_filler_material == 0 or work_order.hours_applied == 0 or work_order.status == "work in progress":
                    print("Please update Work Order before closing the ticket.")
                else:
                    damage_file = self.create_damage_file(work_order)
                    damage_file.print_damage_file_summary()
                pass
            elif menu_selection == "3":
                break
            else:
                print("\nInvalid Selection\n")



    def create_account(self):
        print("*****CREATE CITIZEN ACCOUNT*****")
        name = input("\nName: ")
        address = input("\nAddress: ")
        phone = input("\nPhone Number: ")
        
        citizen = Citizen(name, address, phone)
        self.citizens.append(citizen)
        return citizen

    def login_citizen(self):
        print("*****CITIZEN LOGIN*****")
        name = input("\nName: ")
        phone = input("\nPhone Number: ")
        for citizen in self.citizens:
            if citizen.name == name:
                print("Login Successful...\n\n")
                self.current_user = citizen
                break

    def login_repair_crew(self):
        print("*****REPAIR CREW LOGIN*****")
        name = input("\nCrew Name: ")
        id = int(input("\nID: "))
        for crew in self.repair_crews:
            if crew.name == name and crew.id == id:
                print("Login Successful...\n\n")
                self.current_user = crew
                break


    def report_pothole(self):
        print("*****REPORT A POTHOLE*****")
        street_address = input("Address of Pothole: ")
        size = int(input("Size (1-10): "))
        location = input("Location of Pothole: ")
        pothole = Pothole(self.current_user.id, street_address, size, location)
        self.potholes.append(pothole)
        return pothole

    def assign_repair_crew(self, pothole_priority):
        if pothole_priority == "Low":
            crew_size_required = 3
        elif pothole_priority == "Medium":
            crew_size_required = 6
        elif pothole_priority == "High":
            crew_size_required = 9

        for crew in self.repair_crews:
            if crew.crew_size >= crew_size_required:
                return crew
        pass
        
    def get_assigned_work_orders(self, repair_crew_id):
        assigned_work_orders = []
        for work_order in self.work_orders:
            if work_order.repair_crew_id == repair_crew_id:
                assigned_work_orders.append(work_order)
        return assigned_work_orders

    def get_by_id(self, id, items):
        for item in items:
            if item.id == id:
                return item
        return None

    def print_created_work_order(self, work_order, repair_crew):
        assigned_repair_crew = self.get_by_id(repair_crew.id, self.repair_crews)
        print("Pothole Location: " + work_order.pothole_location)
        print("Pothole Size: " + str(work_order.pothole_size))
        print("Repair Crew Assigned: " + assigned_repair_crew.name)
        print("Work Order Status: " + work_order.status)

    def print_assigned_work_orders(self, assigned_work_orders):
        print("*****ASSIGNED WORK ORDERS*****")
        for work_order in assigned_work_orders:
            print(str(work_order.id) + ". Location: " + str(work_order.pothole_location) + " - Pothole Size: " + str(work_order.pothole_size) + " - Status: " + work_order.status )
        pass
  
    def create_damage_file(self,work_order):
        pothole = self.get_by_id(work_order.pothole_id, self.potholes)
        citizen = self.get_by_id(pothole.citizen_id, self.citizens)
        citizen_name = citizen.name
        citizen_address = citizen.address
        citizen_phone_number = citizen.phone_number
        type_of_damage = work_order.type_of_damage
        dollar_amount_of_damage = work_order.cost_of_repair

        damage_file = Damage_file(citizen_name, citizen_address, citizen_phone_number, type_of_damage, dollar_amount_of_damage)
        self.damage_files.append(damage_file)
        return damage_file

def main():
    phtrs = PHTRS()
    
    phtrs.main_menu()
    pass

if __name__ == '__main__' : main()