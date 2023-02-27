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
# nlp = spacy.load("en_core_web_lg")
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
def get_pos_tag(sentence, tags):
    tokenized = tokenize(sentence)
    return [word for (word, pos) in nltk.pos_tag(tokenized) if pos in tags]

def format_list(list):
    length = len(list)
    if length == 0:
        return ""
    elif length == 1:
        return list[0]
    else:
        return "{}, and {}".format(", ".join(list[:-1]), list[-1])

# Main Function
def handle_input(actor: Actor, input_message: str) -> str:
    ints = predict_class(input_message)
    output_message = get_response(ints, intents)
    intent = ints[0]['intent']

    if intent == 'introduction response':
        name = get_pos_tag(input_message, ['NNP'])
        if len(name) > 0:
            output_message = output_message.replace("<name>", name[0])
    elif intent == 'favorite':
        #subject = get_subject(input_message)
        #output_message = output_message.replace("<noun>", subject)
        pass
    elif intent == 'positive like noun question':
        tags = get_pos_tag(input_message, ['NN', 'NNS', 'NNP', 'NNPS', 'VBG'])
        output_message = output_message.replace("<noun>", format_list(tags))
    elif intent == 'positive want to go place question':
        tags = get_pos_tag(input_message, ['NN', 'NNS', 'NNP', 'NNPS'])
        output_message = output_message.replace("<noun>", format_list(tags))
    elif intent == 'weather question':
        pass

    print([(word, pos) for (word, pos) in nltk.pos_tag(tokenize(input_message))])

    return output_message
