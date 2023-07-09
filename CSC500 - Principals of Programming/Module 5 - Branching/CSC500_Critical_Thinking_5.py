

def main():
    purchased_books = ask_for_integer("How many books did you purchase this month?\n")

    if purchased_books <= 1:
        points_awarded = 0
    elif purchased_books >= 8:
        points_awarded = 60
    elif purchased_books >= 6:
        points_awarded = 30
    elif purchased_books >= 4:
        points_awarded = 15
    elif purchased_books >= 2:
        points_awarded = 5

    print("You have earned", str(points_awarded) + " points for the CSU Global Bookstore this month.")
    pass


def ask_for_integer(text):
    not_number = True
    while not_number: 
        res = input(text)
        try:
            return int(res)        
        except ValueError:
            not_number = True
            print("Please provide an integer as your response.\n")

if __name__ == '__main__' : main()