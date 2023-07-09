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
        self.district = self.__determine_district(address)
        self.repair_priority = self.__determine_repair_priority(size)
        pass
        
    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count

    def __determine_district(self, street_address):
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

    def __determine_repair_priority(self, size):
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
        self.equipment_assigned = self.__assign_equipment(pothole.repair_priority)
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

    def __assign_equipment(self, repair_priority):
        if repair_priority == "Low":
            equipment = "Shovel, Small Truck"
        elif repair_priority == "Medium":
            equipment = "Shovel, Wheelbarrow, Medium Truck"
        elif repair_priority == "High":
            equipment = "Shovel, Wheelbarrow, Large Truck"
        else:
            equipment = ""
        return equipment

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
    count = 0
    def __init__(self, citizen_name, citizen_address, citizen_phone_number, type_of_damage, dollar_amount_of_damage):
        self.id = self.assign_id()
        self.citizen_name = citizen_name
        self.citizen_address = citizen_address
        self.citizen_phone_number = citizen_phone_number
        self.type_of_damage = type_of_damage
        self.dollar_amount_of_damage = dollar_amount_of_damage

    @classmethod
    def assign_id(self):
        self.count +=1
        return self.count
    
class PHTRS_controller():
    
    def __init__(self):
        self.store = PHTRS_store()
        self.view = PHTRS_view()
        self.current_user = None
        

        pass

    def main_menu(self):
        self.view.main_menu_greeting()
        while True:
            menu_selection = self.view.main_menu_selection()

            if menu_selection == "1":
                name, address, phone = self.view.create_account()
                self.store.citizens.append(Citizen(name, address, phone))
            elif menu_selection == "2":
                account_type = self.view.select_account_type()
                if account_type == "1":
                    name, phone = self.view.citizen_login()
                    for c in self.store.citizens:
                        if c.name == name and c.phone_number == phone:
                            self.current_user = c
                            break
                    if self.current_user != None:
                        self.citizen_menu()
                    else:
                        self.view.login_fail()
                    
                elif account_type == "2":
                    name, id = self.view.repair_crew_login()
                    for crew in self.store.repair_crews:
                        if crew.name == name and crew.id == id:
                            self.current_user = crew
                            break
                    if self.current_user != None:    
                        self.repair_crew_menu()
                    else:
                        self.view.login_fail()
            elif menu_selection == "3":
                break
            else:
                self.view.invalid_menu_selection()
        pass

    def citizen_menu(self):
        while True:
            
            menu_selection = self.view.citizen_menu_selection()
            if menu_selection == "1":
                
                pothole = self.view.report_pothole(self.current_user.id)
                self.store.potholes.append(pothole)

                repair_crew = self.assign_repair_crew(pothole.repair_priority)

                work_order = Work_order(pothole, repair_crew)
                self.store.work_orders.append(work_order)
                
                self.view.print_created_work_order(work_order, repair_crew)

            elif menu_selection == "2":
                self.current_citizen = None
                self.view.logout_message()
                break
            else:
                self.view.invalid_menu_selection()
                

        pass

    def repair_crew_menu(self):
        while True:
            assigned_work_orders = self.store.get_assigned_work_orders(self.current_user.id)
            menu_selection = self.view.print_assigned_work_orders(assigned_work_orders)
            
            if menu_selection.isnumeric():
                work_order = self.store.get_by_id(int(menu_selection), self.store.work_orders)
                pothole = self.store.get_by_id(work_order.pothole_id, self.store.potholes)
                if work_order != None:
                    self.work_order_menu(work_order, pothole)
                    pass
            elif menu_selection == "exit":
                self.current_citizen = None
                self.view.logout_message()
                break
            else:
                self.view.invalid_menu_selection()
        pass

    def work_order_menu(self, work_order, pothole):
        while True:
            menu_selection = self.view.work_order_menu(work_order, pothole)
            if menu_selection == "1":
                work_order = self.view.update_work_order(work_order, self.current_user.hourly_rate)
                
                for order in self.store.work_orders:
                    if order.id == work_order.id:
                        order = work_order
                        break
            elif menu_selection == "2":
                if work_order.amount_of_filler_material == 0 or work_order.hours_applied == 0 or work_order.status == "work in progress":
                    self.view.work_order_needs_updating()
                else:
                    damage_file = self.store.create_damage_file(work_order)
                    self.view.print_damage_file_summary(damage_file)
                    break
            elif menu_selection == "3":
                break
            else:
                self.view.invalid_work_order_menu_selection()

    def login_repair_crew(self):
        name, id = self.view.repair_crew_login()

        for crew in self.store.repair_crews:
            if crew.name == name and crew.id == id:
                self.current_user = crew
                break
        if self.current_user != None:
            self.view.login_success_message()
        else:
            self.view.login_fail()




    def assign_repair_crew(self, pothole_priority):
        if pothole_priority == "Low":
            crew_size_required = 3
        elif pothole_priority == "Medium":
            crew_size_required = 6
        elif pothole_priority == "High":
            crew_size_required = 9

        for crew in self.store.repair_crews:
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

class PHTRS_store():
    
    def __init__(self):
        self.citizens = []
        #repair_crews to be sorted by Crew Size in ascending order each time new repair crew is added
        self.repair_crews = [Repair_crew("Small Team", 3, 100),Repair_crew("Medium Team", 6, 200),Repair_crew("Large Team", 9, 300)]
        self.potholes = []
        self.work_orders = []
        self.damage_files = []
        price_of_filler_material = 20
        pass

    

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
    
    def create_damage_file(self, work_order):
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

    def get_by_id(self, id, items):
        for item in items:
            if item.id == id:
                return item
        return None

class PHTRS_view():
    def __init__(self):
        pass
    
    
    #Citizen
    #region 
    def create_account(self):
        print("*****CREATE CITIZEN ACCOUNT*****")
        name = input("\nName: ")
        address = input("\nAddress: ")
        phone = input("\nPhone Number: ")
        return name, address, phone

    def citizen_login(self):
        print("*****CITIZEN LOGIN*****")
        name = input("\nName: ")
        phone = input("\nPhone Number: ")
        return name, phone

    def citizen_menu_selection(self):
        menu_selection = input("\n1. Report New Pothole\n2. Log Out\n")
        return menu_selection

    #endregion


    #Repair Crew
    #region Repair Crew

    def repair_crew_login(self):
        print("*****REPAIR CREW LOGIN*****")
        name = input("\nCrew Name: ")
        id = int(input("\nID: "))
        return name, id


    #endregion

    def report_pothole(self, current_user_id):
        print("*****REPORT A POTHOLE*****")
        street_address = input("Address of Pothole: ")
        size = int(input("Size (1-10): "))
        location = input("Location of Pothole: ")
        pothole = Pothole(current_user_id, street_address, size, location)
        print("\nThank you for your submission. A work order has been created, and a Repair Crew has been assigned.\n\n****Pothole Summary***")
        return pothole

    def print_created_work_order(self, work_order, repair_crew):
        print("Pothole Location: " + work_order.pothole_location)
        print("Pothole Size: " + str(work_order.pothole_size))
        print("Repair Crew Assigned: " + repair_crew.name)
        print("Work Order Status: " + work_order.status)

    def print_assigned_work_orders(self, assigned_work_orders):
        print("*****ASSIGNED WORK ORDERS*****")
        for work_order in assigned_work_orders:
            print(str(work_order.id) + ". Location: " + str(work_order.pothole_location) + " - Pothole Size: " + str(work_order.pothole_size) + " - Status: " + work_order.status )
        return input("\n\nSelect the ID of the Work Order to view the details or select 'exit' to Log Out\n")
        

    def work_order_menu(self, work_order, pothole):
        print("\n*****WORK ORDER SUMMARY*****\n")
        print("Pothole Location: " + pothole.location)
        print("Pothole Size: " + str(pothole.size))
        print("Equipment Assigned: " + work_order.equipment_assigned)
        print("Hours Worked: " + str(work_order.hours_applied))
        print("Amount of Filler Material Used: " + str(work_order.amount_of_filler_material))
        print("Cost of Repair: " + str(work_order.cost_of_repair))
        print("Work Order Status: " + work_order.status )

        menu_selection = input("\n\n1. Update Work Order\n2. Complete Work Order\n3. Go Back to Assigned Work Orders\n")
        return menu_selection
        pass
    
    def update_work_order(self, work_order, hourly_rate):
       hours_applied= input("\nHours to Add: ")
       while True:
           status = input("\nStatus (repaired, temporary repair, not repaired):\n")
           if status in ["repaired", "temporary repair", "not repaired"]:
               break
           else:
               print("\nPlease select a valid status (work in progress, repaired, temporary repair, not repaired)")

       filler_material = input("\nFiller Material Used (Pounds) : ")
       if hours_applied != "":
           hours = work_order.hours_applied + int(hours_applied)
           work_order.hours_applied = hours
       if status != "":
           work_order.status = status
       if filler_material != "":
           work_order.amount_of_filler_material = int(filler_material)


       type_of_damage = input("Type of Damage: ")
       work_order.type_of_damage = type_of_damage

       labor_cost = work_order.hours_applied * hourly_rate
       #Filler Material is sold in 50 pound bags and sold at 20 dollars per 50 pounds
       parts_cost = (work_order.amount_of_filler_material/50) * 20
       work_order.cost_of_repair = labor_cost + parts_cost
       return work_order
       pass

    def print_damage_file_summary(self, damage_file):
        print("\n*****DAMAGE FILE SUMMARY*****")
        print("Citizen Name: " + damage_file.citizen_name)
        print("Citizen Address: " + damage_file.citizen_address)
        print("Citizen Phone Number: " + damage_file.citizen_phone_number)
        print("Type of Damage: " + damage_file.type_of_damage)
        print("Dollar Amount of Damage: " + str(damage_file.dollar_amount_of_damage))



    def main_menu_greeting(self):
        print("*****MAIN MENU*****")
        print("Welcome to the Pothole Tracking and Repair System. Please log in or Create an account to continue.\n")

    def work_order_needs_updating(self):
        print("Please update Work Order before closing the ticket.")

    
    def login_fail(self):
        print("\nLogin Failed. Returning to Login Menu.\n")
    
    def invalid_menu_selection(self):
        print("Invalid Selection\n")

    def main_menu_selection(self):
        menu_selection = input("\n1. Create an Account\n2. Log In\n3. Exit\n")
        return menu_selection

    def select_account_type(self):
        account_type = input("\nSelect 1 to log in as Citizen or 2 for Repair Crew?\n\n1. Citizen\n2. Repair Crew\n")
        return account_type

    def logout_message(self):
        print("Log out successful...")

    def login_success_message(self):
        print("Login Successful...\n\n")

def main():
    phtrs = PHTRS_controller()
    
    phtrs.main_menu()
    pass

if __name__ == '__main__' : main()