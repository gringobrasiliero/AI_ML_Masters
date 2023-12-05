Description:
	- This Chatbot is a Generative, Open-domain Chatbot with a fine-tuned BART model.
	- The intent for this Chatbot is for end users to have an educated, empathetic friend to chat and have small talk with.
	
Data used for Training Model:
		- Cornell Movie Dialogue Corpus
		- Empathetic Dialogues
		- Question-Answer Dataset

Pretrained Model Used for fine-tuning:
	- BART base-sized model (bart-base)

Training Hyperparameters:
	- Learning Rate: 1e-5
	- epochs: 20
	- Early Stopping: Perplexity
	- Batch Size: 40
	
Tokenizer Hyperparameters:
	- Max Length: 100
	- Added Special Tokens: "<user>", "<system>"


Python Modules Used:
	- transformers
	- tensorflow
	- keras
	- numpy
	- pandas
	- sklearn
	- json
	- re
	- os
	- csv
	- pyInstaller
	- warnings
	

	