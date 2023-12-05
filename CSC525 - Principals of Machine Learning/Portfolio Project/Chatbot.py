from transformers import BartTokenizer, TFBartForConditionalGeneration
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import re
import warnings
#Disabling Transformer Logging
from transformers.utils import logging
logging.set_verbosity_info()
logger = logging.get_logger("transformers")
logger.setLevel("ERROR")
logging.disable_progress_bar()
from cleaners import clean_data
from ContextManager import ContextManager
# Suppress Tensorflow Warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="tensorflow")

        
class Chatbot():
    def __init__(self):
        self.model_name = "facebook/bart-base"
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = TFBartForConditionalGeneration.from_pretrained('BartModel')
        
        self.user_token = "<user>"
        self.system_token = "<system>"
        special_tokens = {"additional_special_tokens": [self.user_token, self.system_token]}
        num_added_toks = self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))

        self.max_length = 30
        #temperature values above 1.0 encourages more creative output
        self.temperature = 1.05
        #Repetition Penalty values above 1.0 discourage repetition in generated outputs.
        self.repetition_penalty = 1.2
        self.username = "User: "
        self.conversation_history = []
        pass


    
    def chat(self):
        print("")
        print("Chatbot: Hi! I am your friendly chatbot. Type 'exit' to end the conversation.")
        username = input("Chatbot: Please state your name so I can address you properly.\n" + self.username)
        self.username = username + ": "
        text = ""
        cm = ContextManager()
        while True:
            #Get User Input
            user_input = input(self.username)
            
            #Check for Exit Condition
            if user_input.lower() == 'exit':
                #Ask Consent to use Chat History for future training.
                consent = input("Chatbot: May I use our conversation for future training? (Y for Yes, N for No)\n" + self.username)
                #If Consent granted, do not delete conversation history
                if consent.upper() != "Y":
                    print("Chatbot: Thank you. I will keep our conversation and train on it later.")
                else:
                    print("Chatbot: Okay" + self.username + ". I respect your privacy. Deleting our conversation from memory...")
                    #Consent not granted... Deleting Conversation history
                    self.conversation_history = None
                print("Chatbot: Goodbye!")
                #Breaking the While True loop to end the exit the program
                break
            
            # Prepare input and encode it using the tokenizer
            #Prepend User Token to the user's input
            user_input = self.user_token + " " + user_input
            #Use the context manager to ensure conversation statements do not exceed the token limit.
            #Context manager also cleans the data when data is inserted.
            cm.insert_context(user_input)

            #Get the current inputs, which includes history of the conversation up to 100 tokens.
            history = cm.get_context()

            #Tokenize the input data
            inputs = self.tokenizer(history, add_special_tokens=False, padding='max_length', max_length=self.max_length, truncation=True,return_tensors="tf",repetition_penalty= self.repetition_penalty)

   
            # Generate a response
            with tf.device("/GPU:0"):  # Use GPU if available
                outputs = self.model.generate(inputs.input_ids,attention_mask=inputs.attention_mask, max_length=self.max_length, do_sample = True, temperature=self.temperature)
            
            #Decode the generated output.
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Model is returning incomplete sentences. Removing last sentence if incomplete.
            sentences = re.split(r'(?<=[.!?])\s', response)
            if not re.search(r'[.?!]', sentences[-1]):
                sentences.pop()
            response = " ".join(sentences)

            #Print out the Bots responses
            print("Chatbot: " + response + "\n")

def main():
    chatbot = Chatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()