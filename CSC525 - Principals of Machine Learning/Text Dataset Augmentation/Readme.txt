Text Dataset Augmentation

Description:
	- This program Augments a text dataset by randomly replacing words with a Synonym or deleting words , then saving it into a new text file within the same directory. 
	- This Program:
		1) Grabs a list of files in the "data" directory
		2) Iterates through each file, and if the document is in .txt, .csv, or .json format, will open the document
		3) Program will go through line by line, and if a word is not a Stop word, is a word, and hits the 40% probability, it will use Spacey to grab a list of Synonyms, and replace the word with the first Synonym (if the word has one)
		4) If it did not meet the probability condition, if it meets the probability of 10%, then the word is removed from the dataset.
		5) The program writes each new line into a seperate file.
		


Usage Instructions:
	- Open Command Prompt and navigate to the directory where Critical_thinking5.py exists.
	- execute "python Critical_thinking5.py"
	
	
	