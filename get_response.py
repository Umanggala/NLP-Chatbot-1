from nltk import *

def getResponse(user_query):

    if(user_query == "good morning" or user_query == "Hello"):
        return "Hello, what would you like to eat today?"


    text = user_query
    sents = word_tokenize(text)
    tagged_token = pos_tag(sents)

    for words in tagged_token:
        if(words[1] == "JJ"):
            return "Are you sure you want to eat",words[0],"?"