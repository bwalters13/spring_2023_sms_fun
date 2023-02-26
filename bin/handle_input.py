import os
import random
import json
import pickle
import numpy as np
import nltk
import spacy
from classes.actor import Actor
from keras.models import load_model
from bin.nltk_funcs import tokenize, stem
from bin.train import train_model

# Load Modules
nlp = spacy.load("en_core_web_lg")

# Corpus Data
intents = json.loads(open("data/corpus.json").read())

# Model Data
while True:
    if os.path.exists('data/model.h5'):
        words = pickle.load(open('data/dictionary.pkl', 'rb'))
        classes = pickle.load(open('data/labels.pkl', 'rb'))
        model = load_model('data/model.h5')
        break
    else:
        train_model()

ERROR_THRESHOLD = 0.25
  
# Classification Functions
def clean_up_sentences(sentence):
    sentence_words = tokenize(sentence)
    sentence_words = [stem(word) for word in sentence_words]
    return sentence_words
  
def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)
  
def predict_class(sentence):
    bow = bag_of_words(sentence)

    res = model.predict(np.array([bow]))[0]

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['label'] == tag:                
            result = random.choice(i['outputs'])
            break
    return result

# Helper Functions
def get_name(sentence):
    sent = nlp(sentence.title())
    return " ".join(token.text for token in sent if token.pos_ == 'PROPN')

def get_subject(sentence):
    sentence = nlp(sentence)
    return " ".join(token.text for token in sentence if token.dep_ == 'nsubj')

def get_pos_tag(sentence, tags):
    tokenized = tokenize(sentence)
    return [word for (word, pos) in nltk.pos_tag(tokenized) if pos in tags]

# Main Function
def handle_input(actor: Actor, input_message: str) -> str:
    ints = predict_class(input_message)
    output_message = get_response(ints, intents)
    intent = ints[0]['intent']

    if intent == 'introduction response':
        name = get_name(input_message)
        print(name)
        output_message = output_message.replace("<name>", name)
    elif intent == 'favorite':
        subject = get_subject(input_message)
        output_message = output_message.replace("<noun>", subject)
    elif intent == 'positive like noun question':
        tags = get_pos_tag(input_message, ['NN', 'NNS', 'NNP', 'NNPS', 'VBG'])
        if len(tags) > 0:
            output_message = output_message.replace("<noun>", "{}, and {}".format(", ".join(tags[:-1]), tags[-1]))
    elif intent == 'positive want to go place question':
        tags = get_pos_tag(input_message, ['NN', 'NNS', 'NNP', 'NNPS'])
        if len(tags) > 0:
            output_message = output_message.replace("<noun>", "{}, and {}".format(", ".join(tags[:-1]), tags[-1]))
    elif intent == 'weather question':
        pass

    return output_message
