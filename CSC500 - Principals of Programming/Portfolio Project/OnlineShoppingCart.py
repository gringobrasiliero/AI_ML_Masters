from datetime import date, datetime


def main():
   name = input("What is your name?\n")
   current_date = ask_for_date("What is today's date?\n")

   print("Customer Name:",name)
   print("Today's Date:",current_date.strftime("%B %d, %Y"))
   cart = ShoppingCart(name, current_date)
   shopping_cart_menu(cart)


def get_item_details(item):
    item.item_name = input("Enter the item name:\n")
    item.description = input("Enter the Description of the Item:\n")
    item.item_price = ask_for_number("float", "Enter the item price:\n")
    item.item_quantity = ask_for_number("int", "Enter the item quantity:\n")
    
    return item

def shopping_cart_menu(ShoppingCart):
    while True:
        print("\na - Add item to cart")
        print("r - Remove Item from cart")
        print("c - Change item quantity")
        print("i - Output items' descriptions")
        print("o - Output shopping cart")
        print("q - Quit\n")
        menu_selection = input("Choose an Option:\n")

        if menu_selection == "q":
            break
        elif  menu_selection == "a":
            ShoppingCart.add_item(get_item_details(ItemToPurchase()))
        elif  menu_selection == "r":
            item_to_remove = input("Which Item would you like to remove?\n")
            ShoppingCart.remove_item(item_to_remove)
        elif  menu_selection == "c":
            item_to_edit = ItemToPurchase()
            item_name = input("Which Item do you want to change the quantity for?\n")
            new_item_quantity = ask_for_number("int", "What is the new Item Quantity?\n")
            item_to_edit.item_name = item_name
            item_to_edit.item_quantity = new_item_quantity
            ShoppingCart.modify_item(item_to_edit)
        elif  menu_selection == "i":
            ShoppingCart.print_descriptions()
        elif  menu_selection == "o":
            ShoppingCart.print_total()
        else:
            print("Please enter a valid menu selection.\n")
    print("GoodBye")

def ask_for_number(number_type, text):
    not_number = True
    while not_number: 
        res = input(text)
        try:
            if number_type == "int":
                return int(res)
            elif number_type == "float":
                return float(res)        
        except ValueError:
            not_number = True
            if number_type == "int":
                print("Please provide an integer as your response.\n")
            elif number_type == "float":
                print("Please provide a float as your response.\n")        
            
def ask_for_date(text):
    not_date = True
    while not_date: 
        date_input = input(text)
        try:
            if "/" in date_input:
                current_date = datetime.strptime(date_input, "%m/%d/%Y")
                return current_date
            elif "-" in date_input:
                current_date = datetime.strptime(date_input, "%m-%d-%Y")
                return current_date
            else:
                 print("Please insert a date using m/d/yyyy or m-d-yyyy format.")

        except ValueError:
            print("Please insert a date using m/d/yyyy or m-d-yyyy format.")


class ShoppingCart:
 
    def __init__(self, name, cartDate):
        self.customer_name = name
        self.current_date = cartDate
        self.cart_items = [] 
        pass

    def add_item(self, ItemToPurchase):
        self.cart_items.append(ItemToPurchase)
        pass

    def remove_item(self, item_name):
        try:
            item = next(cart_item for cart_item in self.cart_items if cart_item.item_name == item_name)
            self.cart_items.remove(item)
        except StopIteration: 
            print("Item not found in cart. Nothing removed.")
        pass

    def modify_item(self, ItemToPurchase):
        try:
           item = next(cart_item for cart_item in self.cart_items if cart_item.item_name == ItemToPurchase.item_name)
           if ItemToPurchase.description != "":
               item.description = ItemToPurchase.description
           if ItemToPurchase.item_price != 0.00:
               item.item_price = ItemToPurchase.item_price
           if ItemToPurchase.item_quantity != 0:
               item.item_quantity = ItemToPurchase.item_quantity

        except StopIteration: 
            print("Item not found in cart. Nothing modified.")
        pass

    def get_num_items_in_cart(self):
        num_items = 0
        for item in self.cart_items:
            num_items += item.item_quantity
        return num_items
        
    def get_cost_of_cart(self):
       total = 0
       for i in self.cart_items:
           total += i.item_price * i.item_quantity
       return total 
 
    def print_total(self):
        if len(self.cart_items)==0:
            print("SHOPPING CART IS EMPTY")
        else:
            print(self.customer_name + "'s Shopping Cart - " + self.current_date.strftime("%B %d, %Y"))
            print("Number of Items:", self.get_num_items_in_cart())
            for item in self.cart_items:
                item.print_item_cost()
            print("Total: $" + str(self.get_cost_of_cart()))
        pass

    def print_descriptions(self):
         print(self.customer_name + "'s Shopping Cart - " + str(self.current_date) )
         print("Item Descriptions")
         for item in self.cart_items:
             print(item.item_name + ": " + item.description)
         pass
      
class ItemToPurchase:
    def __init__(self):
        self.item_name = "none"
        self.item_price = 0.00
        self.item_quantity = 0
        self.description = ""
        pass

    def print_item_cost(self):
        subtotal = self.item_quantity * self.item_price
        print(self.item_name, self.item_quantity, "@", "$" + str(self.item_price), "=", "$" + str(subtotal))
        return subtotal

if __name__ == '__main__' : main()


