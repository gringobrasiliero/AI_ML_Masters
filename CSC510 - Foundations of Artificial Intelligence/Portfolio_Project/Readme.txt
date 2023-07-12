
Description:
	-This project uses Computer Vision and a Convolutional Neural Network to:
		1) Extract Characters from an Image
		2) Classify the extracted characters to their digitized value.

Inputs:
	- Image files that are located in the Inputs Directory

Outputs:
	- Text Extracted from the Images provided.

Requirements:
	- inputs/ directory must exist with at least 1 image file
	- character+font+images directory is required to train the model.
		- This directory contains the data the model is trained on.
	- To run program without having to train, the 'text_classifier' directory must exist with the trained model


Modules Used:
	- Numpy
	- Tensorflow
	- Keras
	- OpenCV2
	- imutils
	- csv
	- os

Scope of Inputs:
	- Images must be in .png or .jpg format
	- Text on images must be printed text (No handwriting)
	- Text should be dark text, with lighter background (no white text)


Usage Instructions:
	1) Place images that you want to have text extracted from into the Inputs directory
		- I recommend taking a screenshot of text for easy testing.
		- Sample images are provided in the input folder, so this step is optional.

	2) Open CMD to the Directory where TextDigitizer.py exists on your Computer.

	3) Execute command "python TextDigitizer.py" in the CMD Window.


To Retrain the model:
	1) Download the data set that I used to train the model
		- https://doi.org/10.24432/C5X61Q
	2) Place all downloaded files into a directory called "character+font+images"

	2) Open CMD to the Directory where Classifier.py exists on your Computer.

	3) Execute command "python Classifier.py" in the CMD Window.
		- This will take time to complete.



Information on Data Set used for training:
	- The data set used is a collection of images of characters from 153 character fonts.
	- The data set was used to train the CNN Model to Characterize the characters A-Z upper case, and lower cased.
	- The Licensing for this dataset is under a Creative Commons Attribution 4.0 International license:
		- This means that I can to use the data set as long as I give credit, which I have referenced in this readme.

	- You can view more information about the data set at this link: 
		-  https://doi.org/10.24432/C5X61Q

REFERENCE: 
	Lyman,Richard. (2016). Character Font Images. UCI Machine Learning Repository. https://doi.org/10.24432/C5X61Q.
