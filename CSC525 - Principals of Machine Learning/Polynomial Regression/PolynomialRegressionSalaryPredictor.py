import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

class PolynomialRegressionSalaryPredictor():

    def __init__(self, degrees):
        self.polynomial_features = PolynomialFeatures(degree=degrees)
        self.model = LinearRegression()
        pass

    def load_data(self, file_path):
        # Load the dataset
        data = pd.read_csv(file_path)
        # Extract features and target variable
        self.x = data.iloc[:, 1:2].values  # Years of Experience
        self.y = data.iloc[:, 2].values    # Salary

    def train(self):
        # Fit the polynomial regression model
        poly_features = self.polynomial_features # PolynomialFeatures(degree = self.degrees)
        X_poly = self.polynomial_features.fit_transform(self.x) #Creates matrix of all polynomial combinations of features of x with the specified degree.
        self.model.fit(X_poly, self.y)
        return X_poly


    def predict(self, years_experience):
        # Predict the salary for a given years of experience
        predicted_salary = self.model.predict(self.polynomial_features.transform([[years_experience]]))
        print("Predicted salary for " + str(years_experience) + " years of experience: " + str(predicted_salary[0]))
        return predicted_salary

    def vizualize_data(self, X_poly):
        # Visualize the polynomial regression model (optional, for visualization)
        plt.scatter(self.x, self.y, color='blue', label='Data')
        plt.plot(self.x, self.model.predict(X_poly), color='red', label='Polynomial Regression')
        plt.xlabel('Years of Experience')
        plt.ylabel('Salary')
        plt.title('Polynomial Regression')
        plt.legend()
        plt.draw()
        print("\nShowing a vizualization of the Regression Model.\nPress any key to continue...")
        plt.waitforbuttonpress(0)
        plt.close()

    def evaluate_model(self,x_polynomials):
        y_predictions = self.model.predict(x_polynomials)
        # Calculate R-squared Score
        r2 = r2_score(self.y, y_predictions)
        print("The R-squared score of the data set is " + str(r2) + ".")
        pass

#This function prevents errors from occurring in case end user types in a string where a Float is required.
def ask_for_float(text):
    while True:
        res = input(text)
        if res.isdigit():
            return float(res)
        else:
            print("Please Provide a Number\n\n")

def main():
    #Set Degrees
    degrees=3
    p = PolynomialRegressionSalaryPredictor(degrees)
    #Load the data
    file_path = "position_salaries.csv"
    p.load_data(file_path)

    #Train the Model
    x_polynomials = p.train()

    #Returns an R-squared score using the values and predicted values
    p.evaluate_model(x_polynomials)

    #Vizualization of model
    p.vizualize_data(x_polynomials)

    #Loop to allow end users to have program predict the value of an employee, with the specified number end user puts in.
    while True:
        years_of_exp = ask_for_float("How many years of Experience do you have? Please provide a floating-point number.\n")
        p.predict(years_of_exp)
        quit_program = input("Would you like to try again? (Press 'Y' to try again. Press 'N' to quit\n")
        if quit_program.upper() == "N":
                print("Have a nice day! Goodbye.")
                break
    
    pass

if __name__ == "__main__":
    main()
    

