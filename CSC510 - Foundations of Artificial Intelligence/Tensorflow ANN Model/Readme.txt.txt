Requirements:
	- tensorflow
	- matplotlib

Description: 
	-This program takes the fashion_mnist dataset
		-This dataset is a bunch of images of articles of clothing, with 10 different categories
	-Trains a model (fashion_model) on the dataset
		- If the trained model exists in the directory, then program uses existing trained model, else, trains the model.
		
	- Evaluates the trained model with the Test dataset (Images that the model was not trained on)
		- The Accuracy rate of predicting the articles of clothing, as well as the Loss Function get printed to console.
	-Displays 5 random images of the test dataset, the Predicted category, the Actual category, and the Confidence score the model had for the article of clothing.


Instructions:
	- Execute the python file Critical_Thinking3.py
	- The Accuracy rate of categorizing articles of clothing correctly of the test data set and resulting Loss Function will be printed.
	- 5 random images of the test dataset will be shown with the Predicted category, Actual Category, and Confidence Score.
		- Images are shown by using matplotlib.pyplot.
		- Stats of each of the 5 random images of test dataset also get printed to console.
		
	-If you want to have the Program Train the Model, Remove the folder named "fashion_model" by deleting or renaming the directory.