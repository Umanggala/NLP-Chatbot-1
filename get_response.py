from nltk import *
import speech_recognition as sr

from tkinter import *
import tkinter

import time

from collections import Counter
import random

from gtts import *
import os
import insert_data

def textToSpeech(text_input):
    tts = gTTS(text=text_input,lang='en')
    tts.save('output.mp3')
    os.startfile("output.mp3")
    #os.system("mpg321 output.mp3")

def buttonAction(user_query):

    var = StringVar()
    label = Label(root, textvariable=var, relief=RAISED, bg = 'red')
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

agree_keywords = ["yes", "yeah", "Yes", "yo", "Yo"]
reject_keywords = ["No", "no", "nah"]
location_dict = ["artesia", "hollywood" , "figueroa"]
cuisine_dict = ["italian","mexican","indian","thai", "chinese", "pizza"]
cheap_price = ["cheap", "cheaper", "low", "inexpensive"]
moderate_price = ["moderate"]
high_price = ["expensive", "high"]
current_state = 'none'
cities =  {"Los Angeles":["Los","Angeles"],"santa monica":["santa","monica"],"Marina Del Ray":["Marina","Del","Ray"]}
loc_question_list = ["Where would you like to eat?","Which place you'd like to go today?","What area are you looking for?","Do you have places in your mind?"]
cuisine_question_list = ["Which cuisine would you like to have?","What's cooking on your mind?","Ola amigo, what would like to try today?"]
price_question_list = ["What price category are you looking for?"]
info_dict = {}
global suggestion_dict
suggestion_dict = {}
confirmation = 'none'
update = 'none'

def listenQuery():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    user_query = r.recognize_google(audio)
    var = StringVar()

    label = Label(root, textvariable=var, relief=RAISED, bg='red')
    var.set(user_query)
    label.pack()

    reply = getReponse(user_query)
    var = StringVar()
    label = Message(root, textvariable=var, relief=RAISED, width=1000, bg='green')

    var.set(reply)
    label.pack()


# This function extracts all the relevant info from the user query
# Accordingly, it will design an appropriate response
def getReponse(user_query):

    global current_state                # this could be "location", "cuisine" or "price" depending on which information is not yet provided
    global confirmation
    global suggestion_dict
    global update
    global output

    user_query = user_query.lower()

    if user_query == "good morning":
        textToSpeech("Good morning, how are you doing today?")
        return "Good morning, how are you doing today?"

    else:
        text = user_query
        sents = word_tokenize(text)

        for i in range(len(sents)):
            if sents[i] not in location_dict:
                sents[i] = correction(sents[i])

        tagged_token = pos_tag(sents)

        found_match = False

        for words in tagged_token:
            if found_match:
                cityTest = cityTest
            else:
                cityTest = ''
            found_match = False
            for city in cities.keys():
                if words[0] in cities[city]:
                    cityTest += words[0] + ' '
                    found_match = True
                if cityTest.split(' ')[0:-1] == city.split(' '):
                    print(city)
                    info_dict['Location'] = city

        for words in tagged_token:

            print (words[1])
            if(words[1] == "NNP" or words[1] == "NN" or words[1] == "JJ" or words[1]== "NNS" or words[1] == "DT"):

                # Update the dictionary with all the received information

                if(words[0] in location_dict):
                    info_dict['Location'] = words[0]

                if(words[0] in cuisine_dict):
                    info_dict['Cuisine'] = words[0]

                if(words[0] in cheap_price):
                    info_dict['Price'] = "cheap"

                elif(words[0] in moderate_price):
                    info_dict['Price'] = "moderate"

                elif(words[0] in high_price):
                    info_dict['Price'] = "expensive"

                if(words[0] in agree_keywords):
                    confirmation = "Yes"

                if(words[0] in reject_keywords):
                    confirmation = "No"

                if(words[0] == "location" and current_state == 'update'):
                    update = "Location"

                if(words[0] == "cuisine" and current_state == 'update'):
                    update = "Cuisine"

        if current_state == "update":




            if update == "Location":
                info_dict['Location'] = suggestion_dict['Location']
                output, suggestion_dict = insert_data.set_data(info_dict["Cuisine"],info_dict["Location"],info_dict["Price"])
                textToSpeech(output)
                return output

            elif update == "Cuisine":
                info_dict['Cuisine'] = suggestion_dict['Cuisine']
                output, suggestion_dict = insert_data.set_data(info_dict["Cuisine"],info_dict["Location"],info_dict["Price"])
                return output

            else:
                textToSpeech('Dont blame me if you have a bad experience!')
                textToSpeech('Here are your options')
                textToSpeech(output)
                return output

        if confirmation == "Yes" and current_state == 'confirmation':
            textToSpeech('Ok buddy, I will be back in a minute')
            output, suggestion_dict = insert_data.set_data(info_dict["Cuisine"],info_dict["Location"],info_dict["Price"])

            if(len(suggestion_dict)>0):
                print(suggestion_dict)
                suggestion_string = "Unfortunately ratings of "+info_dict["Cuisine"]+" restaurants at "+info_dict["Location"]+" aren't that great"
                suggestion_string += "\n I would suggest you go to "+suggestion_dict["Location"]+" or try "+suggestion_dict["Cuisine"]+" at "+info_dict["Location"]
                textToSpeech(suggestion_string)
                current_state = "update"
                change_request = "What should I update for you: Location, Cuisine or nothing?"
                textToSpeech(change_request)
                return suggestion_string + change_request
            else:
                textToSpeech('Great choice')
                textToSpeech(output)
                return output

        if confirmation == "No" and current_state == 'confirmation':
            textToSpeech('Sorry for the misunderstanding friend. Where would you want to eat today?')
            current_state = "location"
            info_dict.clear()
            return 'Sorry for the misunderstanding friend. Where would you want to eat today?'

        if current_state == 'location' and 'Location' not in info_dict:
            textToSpeech('Sorry, would you please mention your preferred location?')
            return 'Sorry, would you please mention your preferred location?'

        if current_state == 'cuisine' and 'Cuisine' not in info_dict:
            textToSpeech('I am unable to find restaurants that match your requirements. Try a different cuisine.')
            return 'I am unable to find restaurants that match your requirements. Try a different cuisine.'

        if current_state == 'price' and 'Price' not in info_dict:
            textToSpeech('Sorry, would you please mention your budget?')
            return 'Sorry, would you please mention your budget?'

        if 'Location' not in info_dict:
            current_state = 'location'
            loc_question = random.choice(loc_question_list)
            textToSpeech(loc_question)
            return loc_question
        elif 'Cuisine' not in info_dict:
            current_state = 'cuisine'
            cuisine_question = random.choice(cuisine_question_list)
            textToSpeech(cuisine_question)
            return cuisine_question
        elif 'Price' not in info_dict:
            current_state = 'price'
            price_question = random.choice(price_question_list)
            textToSpeech(price_question)
            return price_question
        else:
            current_state = 'confirmation'
            final_confirmation = 'Is this alright? Cuisine: '+info_dict['Cuisine']+' and Location: '+info_dict['Location']+' and Price:'+info_dict['Price']+'?'
            textToSpeech(final_confirmation)
            return 'Is this alright? Cuisine: '+info_dict['Cuisine']+' and Location: '+info_dict['Location']+' and Price:'+info_dict['Price']+'?'

root = tkinter.Tk()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)

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

C =tkinter.Button(frame, text ="Listen", command = lambda:listenQuery())
C.pack(side = RIGHT)

B =tkinter.Button(frame, text ="Send", command = lambda:buttonAction(v.get()))
B.pack(side = RIGHT)

# background_image = PhotoImage(file="ab.gif")
# label = Label(root, image=background_image)
# label.pack()

root.mainloop()
