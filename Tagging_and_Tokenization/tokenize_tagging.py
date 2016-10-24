'''
import nltk
example = 'Mary had a little lamb'
#for word in example.split():
#        print(word)
text = nltk.word_tokenize(example)
print(nltk.pos_tag(example))
'''

#def match(l,p1):
    #for words in l:


from nltk import *
text = "I would like to eat Mexican today"
sents = word_tokenize(text)
tagged_token = pos_tag(sents)

for words in tagged_token:
    if(words[1] == "JJ"):
        print(words)

#print(match(tagged_token,"JJ"))



