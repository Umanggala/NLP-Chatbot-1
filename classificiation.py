import numpy as np
import csv, sys
import pandas as pd
import sklearn, scipy
from sklearn import linear_model, datasets

dialogue_acts = pd.read_csv('temp.csv', sep=',', header=None)

data = dialogue_acts.ix[:,range(dialogue_acts.shape[1]-1)].values
train_Y = dialogue_acts.ix[:,dialogue_acts.shape[1]-1].values
distinct_words = {}

count = 0

for i in range(data.shape[0]):
    sentence = data[i,0]
    split_sentence = sentence.split(" ")

    for j in range (len(split_sentence)):
        current_word = split_sentence[j]
        if current_word not in distinct_words:
            distinct_words[current_word] = count
            count += 1

train_X = np.zeros(shape=(0,len(distinct_words)))

for i in range(data.shape[0]):
    sentence = data[i,0]
    split_sentence = sentence.split(" ")
    current_row = np.zeros(shape=(1,len(distinct_words)))

    for word in split_sentence:
        print(word)
        index = distinct_words[word]
        print(index)
        current_row[0,index] = 1

    train_X = np.concatenate((train_X, current_row), axis=0)

print(train_X)
print(train_Y)

logreg = linear_model.LogisticRegression(C=1)
logreg.fit(train_X, train_Y)

input_sentence = "I want to eat Chinese today"

split_input = input_sentence.split(" ")

input_row = np.zeros(shape=(1,len(distinct_words)))

for word in split_input:
    index = distinct_words[word]
    input_row[0,index] = 1

output_label = logreg.predict(input_row)
print(output_label)