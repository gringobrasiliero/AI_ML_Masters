import random
import spacy
from nltk.corpus import wordnet
import os
from spacy.lang.en import stop_words

class TextAugmentor():
    def __init__(self):
        self.data_directory = "data/"
        self.nlp = spacy.load("en_core_web_sm")
        self.probability_of_synonym_change = 0.4
        self.probability_of_deletion = 0.05
        self.stop_words = stop_words.STOP_WORDS

    # Function to get synonyms of a word using NLTK's WordNet
    def get_synonyms(self, word):
        synonyms = []
        for synonym in wordnet.synsets(word):
            for lemma in synonym.lemmas():
                synonyms.append(lemma.name())
        return synonyms


    #Augments Line by replacing random words with synonym  or randomly removing words. Does not remove or alters stop words..
    def augment_line(self, sentence):
        doc = self.nlp(sentence)
        new_line = []
    
        for token in doc:
            #If no special characters in word and token not a stop word
            if token.is_alpha and token not in self.stop_words:
                if random.random() < self.probability_of_synonym_change:
                    synonyms = self.get_synonyms(token.text)
                    if synonyms:
                        new_word = random.choice(synonyms)
                        new_line.append(new_word)
                    else:
                        new_line.append(token.text)
                elif random.random() < self.probability_of_deletion:
                    #'Deletes' Word by not appending the word to the new line
                    pass
                else: 
                    new_line.append(token.text)

            else:
                #Adds word to the new line
                new_line.append(token.text)
        new_line_text = ' '.join(new_line)
        return new_line_text

    def augment_data_directory(self, directory):
        file_list = os.listdir(directory)
        print(file_list)
        accepted_file_extensions = ('.txt', '.csv', '.json')
        for file in file_list:
            if file.endswith(accepted_file_extensions):
                full_file_path = directory + file
                new_file_path = directory + "new" + file

                new_file = open(new_file_path, "w")

                with open(full_file_path, "r", encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        print(line)
                        new_line = self.augment_line(line)
                        new_file.write(new_line)
        pass


def main():

    t = TextAugmentor()
    directory = 'data/'
    t.augment_data_directory(directory)



        

if __name__ == "__main__":
    main()