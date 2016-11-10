from nltk import *

from tkinter import *
import tkinter

import time

from collections import Counter
import random

def buttonAction(user_query):

    var = StringVar()
    label = Label( root, textvariable=var, relief=RAISED, bg = 'red')
    var.set(user_query)
    label.pack()

    reply = getReponse(user_query)
    var = StringVar()
    label = Message(root, textvariable=var, relief=RAISED, width = 1000, bg = 'green')

    var.set(reply)
    label.pack()

# This function will check the current time and return a greeting message accordingly (eg. Good Morning or Good Afternoon)
def getTime(user_offset, system_time):
    user_time = system_time + (user_offset*60*60)
    user_hour = time.gmtime(user_time)[3]

    if 5 <= user_hour < 12:
        return 'Good morning, how may I help you today?'
    elif 12 <= user_hour < 16:
        return 'Good afternoon, how may I help you today?'
    elif 16 <= user_hour < 24:
        return 'Good evening, how may I help you today?'


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
current_state = 'none'
loc_question_list = ["Where would you like to eat?","Which place you'd like to go today?","What area are youb looking for?","Do you have places in your mind?"]
cuisine_question_list = ["Which cuisine would you like to have?","What's cooking on your mind?","Which country food would you like to have for your taste bud?","Ola amigo, what would like to try today?"]
info_dict = {}


# This function extracts all the relevant info from the user query
# Accordingly, it will design an appropriate response
def getReponse(user_query):

    global current_state

    user_query = user_query.lower()

    if user_query == "good morning":
        return "Good morning, how are you doing today?"

    else:
        text = user_query
        sents = word_tokenize(text)

        for i in range(len(sents)):
            if sents[i] not in location_dict:
                sents[i] = correction(sents[i])


        tagged_token = pos_tag(sents)
        for words in tagged_token:
            if(words[1] == "NNP" or words[1] == "NN" or words[1] == "JJ"):

                if(words[0] in location_dict):
                    info_dict['Location'] = words[0]

                if(words[0] in cuisine_dict):
                    info_dict['Cuisine'] = words[0]

        if current_state == 'location' and 'Location' not in info_dict:
            return 'Sorry, would you please mention your preferred location?'

        if current_state == 'cuisine' and 'Cuisine' not in info_dict:
            return 'I am unable to find restaurants that match your requirements. Try a different cuisine.'

        if 'Location' not in info_dict:
            current_state = 'location'
            loc_question = random.choice(loc_question_list)
            return loc_question
        elif 'Cuisine' not in info_dict:
            current_state = 'cuisine'
            cuisine_question = random.choice(cuisine_question_list)
            return cuisine_question
        else:
            return 'Is this alright? Cuisine: '+info_dict['Cuisine']+' and Location: '+info_dict['Location']


root = tkinter.Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

# Create the text field where user will enter his query
v = StringVar()

E1 = Entry(frame, bd =5, textvariable= v)
E1.pack(side = LEFT)


# offset time is -8 for PST
greeting_message = getTime(-8, time.time())

# The bot begins the conversation
var = StringVar()
label = Label( root, textvariable=var, relief=RAISED)
var.set(greeting_message)
label.pack()

# We then extract the user query and call the getResponse function

B =tkinter.Button(frame, text ="Send", command = lambda:buttonAction(v.get()))
B.pack(side = RIGHT)

root.mainloop()

