import os
import random
import json
import pickle
import numpy as np
import nltk
import requests
import re
from classes.actor import Actor
from keras.models import load_model
from bin.nltk_funcs import tokenize, stem, split_sentences
from bin.train import train_model
from nltk.tag.stanford import StanfordNERTagger

# NLTK
nertTagger = StanfordNERTagger('data/stanford-ner/classifiers/english.all.3class.caseless.distsim.crf.ser.gz', 'data/stanford-ner/stanford-ner.jar')

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

    res = model.predict(np.array([bow]), verbose=0)[0]

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
    error_result = ""
    for i in list_of_intents:
        if i['label'] == tag:                
            result = random.choice(i['outputs'])

            if "error_outputs" in i:
                error_result = random.choice(i['error_outputs'])
            break

    return result, error_result

# Helper Functions
def get_ner_tag(sentence, tags):
    return [word for (word, pos) in nertTagger.tag(tokenize(sentence)) if pos in tags]

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
    sentences = split_sentences(input_message)

    output_messages = []

    for sentence in sentences:
        ints = predict_class(sentence)
        output_message, error_message = get_response(ints, intents)
        intent = ints[0]['intent']

        if intent == 'introduction response':
            name = get_ner_tag(sentence, ['PERSON'])
            if len(name) > 0:
                output_message = output_message.replace("<name>", name[0])
            else:
                output_message = error_message
        elif intent == 'favorite':
            subject = get_pos_tag(input_message, ['NN', 'NNS', 'NNP'])
            if len(subject) > 0:
                output_message = output_message.replace("<noun>", subject[0])
            else:
                output_message = error_message
        elif intent == 'colors response':
            subject = get_pos_tag(input_message, ['JJ','NN', 'NNS', 'NNP'])
            if len(subject) > 0:
                output_message = output_message.replace("<color>", subject[0])
            else:
                output_message = error_message
        elif intent == 'positive like noun question':
            tags = get_pos_tag(sentence, ['NN', 'NNS', 'NNP', 'NNPS', 'VBG'])
            output_message = output_message.replace("<noun>", format_list(tags))
        elif intent == 'positive want to go place question':
            locations = list(set(get_ner_tag(sentence, ['LOCATION']) + get_pos_tag(sentence, ['NN', 'NNS', 'NNP', 'NNPS'])))
            if len(locations) > 0:
                output_message = output_message.replace("<noun>", format_list(tags))
            else:
                output_message = error_message
        elif intent == 'weather question':
            location = get_ner_tag(sentence, ['LOCATION'])

            if len(location) > 0:
                location = location[0]
            else:
                location = "San Marcos"

            # Create Google Query
            url = f"https://www.google.com/search?q=weather+{location}"
            html = requests.get(url).text

            temperature = re.search(r'class="BNeawe iBp4i AP7Wnd">([0-9]+.*?)</div>', html)
            if temperature:
                temperature = temperature.group(1)

                output_message = output_message.replace("<location>", location)
                output_message = output_message.replace("<temperature>", temperature)

        output_messages.append(output_message)

    return output_messages
