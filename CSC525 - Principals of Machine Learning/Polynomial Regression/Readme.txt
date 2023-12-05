Simple Polynomial Regression in Python

Description:
	- This program uses Polynomial Regression to predict the value of an employee candidate based on the years of experience.
	- This Program:
		1) "Trains" the model by loading the "Level" (X) and "Salary" (Y) columns from the position_salaries.csv data set.
			- "Level" Column represents the Years of Experience
			- "Salary" Column represents the Annual Salary
			- The "Position" Column is not used.
		2) Evaluates the model by returning the R-Squared Score.
		3) Shows a visualization of the data set with polynomial regression line.
		4) Allows end user to plug in their years of experience to get the estimated salary based on the model that was trained.

Data Source:
	- The data used for the Positions Salaries Dataset was acquired at https://s3.us-west-2.amazonaws.com/public.gamelab.fun/dataset/position_salaries.csv

Usage Instructions:
	- Open Command Prompt and navigate to the directory where PolynomialRegressionSalaryPredictor.py exists.
	- execute "python PolynomialRegressionSalaryPredictor.py"
	- When done looking at the generated graph, press any key to continue.
	- Answer the prompts from the running program, inputting floating point numbers for the years of experience you would like to get predicted salary on.
	- After the program gives you the results, you will have the option to exit the program by inserting "N". 
		- You can also exit by pressing Control+C.