import re

def clean_data(data):
    #To Lowercase
    data = data.lower()
    #Removing Leading and trailing white-space
    data = data.strip()
    #Seperating Punctuation from words
    data = re.sub(r"\?", " ?", data)
    data = re.sub(r"\.", " .", data)
    data = re.sub(r"\,", " ,", data)
    data = re.sub(r"!", " !", data)

    #Removing Double White Spaces.
    data = re.sub(r"  ", " ", data)
    data = re.sub(r"  ", " ", data)
    data = re.sub(r"  ", " ", data)
    data = re.sub(r"  ", " ", data)
    data = re.sub(r"  ", " ", data)
    
    #Removing contractions - All Text is lower cased at this point
    data = re.sub(r"he's", "he is", data)
    data = re.sub(r"there's", "there is", data)
    data = re.sub(r"we're", "we are", data)
    data = re.sub(r"that's", "that is", data)
    data = re.sub(r"won't", "will not", data)
    data = re.sub(r"they're", "they are", data)
    data = re.sub(r"can't", "cannot", data)
    data = re.sub(r"wasn't", "was not", data)
    data= re.sub(r"aren't", "are not", data)
    data = re.sub(r"isn't", "is not", data)
    data = re.sub(r"what's", "what is", data)
    data = re.sub(r"haven't", "have not", data)
    data = re.sub(r"hasn't", "has not", data)
    data = re.sub(r"there's", "there is", data)
    data = re.sub(r"he's", "he is", data)
    data = re.sub(r"it's", "it is", data)
    data = re.sub(r"you're", "you are", data)
    data = re.sub(r"i'm", "i am", data)
    data = re.sub(r"shouldn't", "should not", data)
    data = re.sub(r"wouldn't", "would not", data)
    data = re.sub(r"i'm", "i am", data)
    data = re.sub(r"i'm", "i am", data)
    data = re.sub(r"isn't", "is not", data)
    data = re.sub(r"here's", "here is", data)
    data = re.sub(r"you've", "you have", data)
    data = re.sub(r"we're", "we are", data)
    data = re.sub(r"what's", "what is", data)
    data = re.sub(r"couldn't", "could not", data)
    data = re.sub(r"we've", "we have", data)
    data = re.sub(r"who's", "who is", data)
    data = re.sub(r"y'all", "you all", data)
    data = re.sub(r"would've", "would have", data)
    data = re.sub(r"it'll", "it will", data)
    data = re.sub(r"we'll", "we will", data)
    data = re.sub(r"we've", "we have", data)
    data = re.sub(r"he'll", "he will", data)
    data = re.sub(r"y'all", "you all", data)
    data = re.sub(r"weren't", "were not", data)
    data = re.sub(r"didn't", "did not", data)
    data = re.sub(r"they'll", "they will", data)
    data = re.sub(r"they'd", "they would", data)
    data = re.sub(r"don't", "do not", data)
    data = re.sub(r"they've", "they have", data)
    data = re.sub(r"i'd", "i would", data)
    data = re.sub(r"should've", "should have", data)
    data = re.sub(r"where's", "where is", data)
    data = re.sub(r"we'd", "we would", data)
    data = re.sub(r"i'll", "i will", data)
    data = re.sub(r"weren't", "were not", data)
    data = re.sub(r"they're", "they are", data)
    data = re.sub(r"let's", "let us", data)
    data = re.sub(r"it's", "it is", data)
    data = re.sub(r"can't", "cannot", data)
    data = re.sub(r"don't", "do not", data)
    data = re.sub(r"you're", "you are", data)
    data = re.sub(r"i've", "i have", data)
    data = re.sub(r"_comma_", ", ", data)
    data = re.sub(r"that's", "that is", data)
    data = re.sub(r"i'll", "i will", data)
    data = re.sub(r"doesn't", "does not",data)
    data = re.sub(r"i'd", "i would", data)
    data = re.sub(r"didn't", "did not", data)
    data = re.sub(r"ain't", "am not", data)
    data = re.sub(r"you'll", "you will", data)
    data = re.sub(r"i've", "i have", data)
    data = re.sub(r"don't", "do not", data)
    data = re.sub(r"i'll", "i will", data)
    data = re.sub(r"i'd", "i would", data)
    data = re.sub(r"let's", "let us", data)
    data = re.sub(r"you'd", "you would", data)
    data = re.sub(r"it's", "it is", data)
    data = re.sub(r"ain't", "am not", data)
    data = re.sub(r"haven't", "have not", data)
    data = re.sub(r"could've", "could have", data)
    data = re.sub(r"you've", "you have", data)
    return data
    

