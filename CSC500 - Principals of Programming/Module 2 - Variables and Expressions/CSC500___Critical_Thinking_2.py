
def main():
    subtotal = get_subtotal()
    sales_tax = get_sales_tax(subtotal)
    total = get_total(subtotal, sales_tax)

    print("The Subtotal is $" + str(subtotal))
    print("The Sales Tax is: $" + str(sales_tax))
    print("The Total price is: $" + str(total))
    pass

def get_subtotal():
    subtotal = 0
    i = 1
    while i <= 5:
        text = "What is the price for Item #" + str(i) + "? "
        item_price = ask_item_price(text)
        subtotal += item_price        
        i += 1
    return round(subtotal,2)

def get_sales_tax(subtotal):
    sales_tax = subtotal *.07
    return round(sales_tax, 2)
    
def get_total(subtotal, sales_tax):
    total = round(subtotal + sales_tax,2)
    return total

def ask_item_price(text):
    not_number = True
    while not_number: 
        res = input(text)
        try:
            return float(res)        
        except ValueError:
            not_number = True
            print("Please provide a valid price.\n")

if __name__ == '__main__' : main()

