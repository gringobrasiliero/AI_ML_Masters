from random import randint
from sklearn.linear_model import LinearRegression

def data_creator(TRAIN_SET_COUNT, coefficients):
    numbers = [0,0,0]
    rand_max = 100
    TRAIN_INPUT = list()
    TRAIN_OUTPUT = list()
    for i in range(TRAIN_SET_COUNT):
        row = []
        for j in range(len(coefficients)):
            random_num = randint(0, rand_max)
            row.append(random_num)
        op = solve_equation(row, coefficients)
        
        TRAIN_INPUT.append(row)
        TRAIN_OUTPUT.append(op)
    return TRAIN_INPUT, TRAIN_OUTPUT



def solve_equation1(numbers, coefficients):
    #Assigning Numbers
    a = numbers[0]
    b = numbers[1]
    c = numbers[2]
    d = numbers[3]    
    
    #Assigning Coefficients
    c1 = coefficients[0]
    c2 = coefficients[1]
    c3 = coefficients[2]
    c4 = coefficients[3]    
    
    #Calcuating
    op = (a * c1) + (b * c2) + (c * c3) + (d * c4)
    return op

def solve_equation(numbers, coefficients):
    value=0
    for i in range(len(numbers)):
        value += numbers[i] * coefficients[i]
    return value

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

def train_model(TRAIN_INPUT, TRAIN_OUTPUT):
    model = LinearRegression(n_jobs=-1) #n_jobs =-1 uses all available cores for faster computation
    model.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)
    return model

def get_user_input_nums(noun, number_of_variables):
    numbers = []
    for i in range(number_of_variables):
        number = ask_for_number("float","What is " + noun + " #" + str(i+1) + "?\n")
        numbers.append(number)
    return numbers

def main():
    TRAIN_SET_COUNT = 1000
    number_of_variables = 0
    
    intro = "Hello. I will predict the coefficients and the value of the equation ((a * c1) + (b * c2) + (c * c3) + (d * c4)...), from 4-8 variables."
    print(intro)
    print("\nYou will\n\t1) Select the number of Variables to be used.\n\t2) Select the Coefficients\n\t3) After I train, you will select the values to the variables. I will then predict the value, and show the actual value.\n")
    while True:
        number_of_variables = ask_for_number("int", "How many variables do you want included? (Please select an integer from 4-8)\n")
        if number_of_variables < 4 or number_of_variables > 8:
            print("Please select an integer in between the values of 4 and 8...")
        else:
            break

    #Get User's coefficients
    noun = "Coefficient"
    coefficients = get_user_input_nums(noun, number_of_variables)
    


    print("\nThank you. After some data is generated, I will train.\n")
    TRAIN_INPUT, TRAIN_OUTPUT = data_creator(TRAIN_SET_COUNT, coefficients)

    model = train_model(TRAIN_INPUT, TRAIN_OUTPUT)
    print("Training Complete.\n")
    print("Okay, give me some numbers for the equation, so I can predict.\n")
    noun = "Test Number"
    X_TEST = get_user_input_nums(noun, number_of_variables)
    
    actual_result = solve_equation(X_TEST, coefficients)

    predicted_result = model.predict(X=[X_TEST])
    predicted_coefficients = model.coef_


    print("Actual result:",actual_result)
    print("Predicted Result:",predicted_result)
    print()
    print("Actual Coefficients:",coefficients)
    print("Predicted Coefficients:",predicted_coefficients)

    


    
if __name__ == "__main__":
    main()