
def main():
    current_hour = ask_for_integer("What is the current hour? ")
    hours_until_alarm = ask_for_integer("How many hours do you want the alarm to wait for? ")
        
    result = current_hour + hours_until_alarm
    if result > 24:
        result %= 24
        print("The alarm will go off at", str(result) + ":00." )
    else: 
        print("The alarm will go off at", str(result) + ":00." )
    
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