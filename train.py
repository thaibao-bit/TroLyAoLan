from builtins import print
from tabnanny import verbose
import nltk
from underthesea import word_tokenize
from nltk.stem import WordNetLemmatizer # change to underthesea library
import numpy as np
import tflearn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
import json
import pickle


with open("intents.json") as file:
    intents = json.load(file)

words = []
labels = []
docs = []

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wrds = word_tokenize(pattern)
        words.extend(wrds)
        docs.append((wrds, intent["tags"]))

        if intent["tags"] not in labels:
            labels.append(intent["tags"])


words = sorted(set(words))

labels = sorted(set(labels))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(labels, open('labels.pkl', 'wb'))

training = []
output_empty = [0] *len(labels)

for doc in docs:
    bag = []
    word_patterns = doc[0]
    word_patterns = [word.lower() for word in word_patterns]

    for word in words:
        if word in word_patterns:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[labels.index(doc[1])] = 1
    training.append([bag,output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()

model.add(Dense(128, input_shape = (len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))

model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(len(train_y[0]), activation = 'softmax'))

sgd = SGD(lr=0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics=['accuracy'])


hist = model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size = 5, verbose =1)


model.save('chatbot.h5', hist)
pickle.dump({'words':words, 'classes':labels, 'train_x':train_x, 'train_y':train_y}, open( "bot-data.pkl", "wb" ))
print("Done")

