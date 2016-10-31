from nltk import *

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

location_dict = ["artesia", "hollywood" , "figueroa"]
cuisine_dict = ["italian","mexican","indian","american"]

info_dict = {}

def getReponse(user_query):


    user_query = user_query.lower()

    if user_query == "good morning":
        return "Good morning, how are you doing today?"

    else:
        text = user_query
        sents = word_tokenize(text)
        print (sents)

        for word in sents:
            word = correction(word)
            print (word)

        tagged_token = pos_tag(sents)
        for words in tagged_token:
            if(words[1] == "NNP" or words[1] == "NN" or words[1] == "JJ"):
                if(words[0] in location_dict):
                    info_dict['Location'] = words[0]

                if(words[0] in cuisine_dict):
                    info_dict['Cuisine'] = words[0]

        if 'Location' not in info_dict:
            return 'Which area?'
        elif 'Cuisine' not in info_dict:
            return 'Which cuisine would you like to have?'
        else:
            return 'Is this alright? Cuisine: '+info_dict['Cuisine']+'and Location: '+info_dict['Location']

from tkinter import *
import tkinter


root = tkinter.Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# Create the text field where user will enter his query
v = StringVar()

E1 = Entry(frame, bd =5, textvariable= v)
E1.pack(side = LEFT)

def buttonAction(user_query):

    reply = getReponse(user_query)
    var = StringVar()
    label = Message( root, textvariable=var, relief=RAISED, width = 1000)

    var.set(reply)
    label.pack()

B = tkinter.Button(frame, text ="Send", command = lambda:buttonAction(v.get()))
B.pack(side = RIGHT)

root.mainloop()

