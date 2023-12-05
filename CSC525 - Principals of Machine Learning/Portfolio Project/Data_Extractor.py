import json
import pandas as pd
from cleaners import clean_data
import re
from ContextManager import ContextManager

class Data_Extractor():
    def __init__(self):
        self.training_data_path = 'training_data.csv'
        #used to limit History of Conversation
        self.max_length = 100

        # Define user and system tokens
        self.user_token = "<user>"
        self.system_token = "<system>"

        pass

    def read_QA_dataset(self, filepath):
        columns = ['Input', 'Output']
        parsed_data = pd.DataFrame(columns=columns)
        

        # Read the text file as if it were a CSV
        index = ['Input']
        delimiter = '\t'
        df = pd.read_csv(filepath, delimiter=delimiter)
        rows, columns = df.shape
        for i in range(1, rows):
            row = df.iloc[i]
            input_text = str(row['Question'])
            output_text = str(row['Answer'])

            #Skipping rows that = NULL
            if input_text  == "NULL" or output_text  == "NULL" or input_text  == "nan" or output_text  == "nan":
                continue

            input_text = self.user_token + " " + str(row['Question'])
            input_text = clean_data(input_text)
            #Limit to Max word Limit
            input_text = list(input_text.split(" "))[:self.max_length]
            input_text = " ".join(map(str,input_text))
            
            output_text = self.system_token + " " + str(row['Answer'])
            #Limit to Max word Limit     
            output_text = clean_data(output_text)
            output_text = list(output_text.split(" "))[:self.max_length]
            output_text = " ".join(map(str,output_text))
            
            new_row = pd.DataFrame({"Input": input_text, "Output": output_text},index=index)
            parsed_data = pd.concat([parsed_data, new_row], ignore_index=True)
        return parsed_data
    
    def read_movie_corpus(self, file_path):
        cm = ContextManager()
        # Create an empty dataframe with column names
        columns = ['Input', 'Output']
        parsed_data = pd.DataFrame(columns=columns)
        inputs = []
        outputs = []

        df = pd.read_json(file_path, lines=True)
        index = ['Input']
        
        rows, columns = df.shape
        print("Total Rows:",rows)
        input_text=""
        history=""

        unique_conversations = df['conversation_id'].unique()
        c_rows = unique_conversations.shape
        print("# of Conversations:",c_rows)
        c=1
        for convo_id in unique_conversations:
            c+=1
            if c%1000==0:
                #Printing progress
                print(c)
            #Clearing out Context for each conversation
            cm.clear_context()
            mask = df['conversation_id'] == convo_id
            conversation = df[mask]
            rows, columns = conversation.shape
            for i in range(1, rows,2):
                row1 = conversation.iloc[i-1]
                row2 = conversation.iloc[i]

                input_text = self.user_token + " " + row1['text']
                output_text = self.system_token + " " + row2['text']
            
                #Inserting input
                cm.insert_context(input_text)

                output_text = clean_data(output_text)
                #Limit to Max word Limit     
                output_text = list(output_text.split(" "))[:self.max_length]
                output_text = " ".join(map(str,output_text))
                
                #Get History of current conversation
                history = cm.get_context()

                #Add New Row            
                new_row = pd.DataFrame({"Input": history, "Output": output_text},index=index)
                parsed_data = pd.concat([parsed_data, new_row], ignore_index=True)

                #Insert output text to context
                cm.insert_context(output_text)

        return parsed_data


    def read_empathy(self, filepath):
        df = pd.read_csv(filepath,index_col=0)
        column_names = df.columns.tolist()
        rows, columns = df.shape
        print("Total Rows:",rows)

        #Removing Rows that leaked text to the next column. 
        df = df[df['Unnamed: 5'] != ""]
        print()
        #Removing Extra Columns
        columns_to_remove = ['Unnamed: 5','Unnamed: 6']
        df = df.drop(columns=columns_to_remove, axis=1)
        
        columns = ['Input', 'Output']
        parsed_data = pd.DataFrame(columns=columns)

        #Sets index Column of Data frame used when creating the new_row
        index = ['Input']
        rows, columns = df.shape
        history = ""

        cm = ContextManager()
        unique_conversations = df['Situation'].unique()
        for convo_id in unique_conversations:
            cm.clear_context()
            mask = df['Situation'] == convo_id
            conversation = df[mask]
            rows, columns = conversation.shape
            rows -= 1 #Last row of conversation is just repeated data
            for i in range(rows): 
                row1 = conversation.iloc[i]

                input_text = str(row1['empathetic_dialogues'])
                #Removing Customer and Agent text that is within this dataset
                input_text = input_text.replace("Customer :","")
                input_text = input_text.replace("Agent :","")
                #Prepending User Token
                input_text = self.user_token + " " + input_text
                #Inserting input into the context
                cm.insert_context(input_text)
                #Get Current context
                history = cm.get_context()
                #Prepend System Token to output
                output_text = self.system_token + " " + str(row1['labels'])
                output_text = clean_data(output_text)

                #Getting list of words with max len limit
                output_text= list(output_text.split(" "))[:self.max_length]
                output_text = " ".join(map(str,output_text))

                new_row = pd.DataFrame({"Input": history, "Output": output_text},index=index)
                parsed_data = pd.concat([parsed_data, new_row], ignore_index=True)
                #Insert the output text into the context of conversation
                cm.insert_context(output_text)
        return parsed_data
    

    def process_and_combine_datasets(self):

        #MOVIE CORPUS###############################
        file_path = "test_data/utterances.jsonl"
        parsed_data = self.read_movie_corpus(file_path)
        ##Write to CSV
        parsed_data = parsed_data.dropna()
        parsed_data.to_csv(self.training_data_path, index=False, mode='w') #Writing File
        print("Movie Corpus Complete")
        #Clearing out Dataframe to help with Memory
        parsed_data = pd.DataFrame()

        #QA Datasets###############################
        qa_datasets = ["test_data/Question_Answer_Dataset_v1.2/S08/question_answer_pairs.txt", "test_data/Question_Answer_Dataset_v1.2/S09/question_answer_pairs.txt", "test_data/Question_Answer_Dataset_v1.2/S10/question_answer_pairs.txt" ]
        for file_path in qa_datasets:
            parsed_data = self.read_QA_dataset(file_path)
            parsed_data = parsed_data.dropna()
            #Write to CSV
            parsed_data.to_csv(self.training_data_path, index=False, mode='a') #Appending to File
            print(file_path,"QA Dataset Complete")

            #Clearing out Dataframe to help with Memory
            parsed_data = pd.DataFrame()



        #Emotional Dialogues###############################
        file_path = 'test_data/emotion-emotion_69k.csv'
        parsed_data = self.read_empathy(file_path)
        parsed_data = parsed_data.dropna()
        #Write to CSV
        parsed_data.to_csv(self.training_data_path, index=False, mode='a')  # Appending to File
        print("Empathy Complete")

        #Clearing out Dataframe to help with Memory
        parsed_data = pd.DataFrame()

def main():
    de = Data_Extractor()
    de.process_and_combine_datasets()

 
if __name__ == "__main__":
    main()