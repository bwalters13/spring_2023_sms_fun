import nltk
import json
import random
import numpy as np
import pickle

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from nltk_funcs import tokenize, stem

# Load Corpus.json
with open('data/corpus.json', 'r') as file:
    corpus = json.load(file)

# Parse Json Data
dictionary = []
labels = []
documents = []
ignored_words = ["?", "!", ".", ","]

for intent in corpus['intents']:
    label = intent['label']
    labels.append(label)

    for input in intent['inputs']:
        word_list = tokenize(input)
        dictionary.extend(word_list)
        documents.append((word_list, label))
  
dictionary = [stem(word) for word in dictionary if word not in ignored_words]
dictionary = sorted(set(dictionary))
labels = sorted(set(labels))

pickle.dump(dictionary, open('dictionary.pkl', 'wb'))
pickle.dump(labels, open('labels.pkl', 'wb'))

training = []
output_empty = [0]*len(labels)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [stem(word.lower()) for word in word_patterns]

    for word in dictionary:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[labels.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
  
# splitting the data
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Train Model
# creating a Sequential machine learning model
model = Sequential()
model.add(Dense(64, input_shape=(len(train_x[0]), ), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
  
# compiling the model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5)
  
# saving the model
model.save("model.h5", hist)