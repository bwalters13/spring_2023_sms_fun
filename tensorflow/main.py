import random
import json
import pickle
import numpy as np
import nltk
from keras.models import load_model
from train.nltk_funcs import tokenize, stem
import spacy

nlp = spacy.load("en_core_web_lg")

intents = json.loads(open("data/corpus.json").read())
words = pickle.load(open('dictionary.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))
model = load_model('model.h5')
  
def clean_up_sentences(sentence):
    sentence_words = tokenize(sentence)
    sentence_words = [stem(word)
                      for word in sentence_words]
    return sentence_words
  
def bagw(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0]*len(words) # Words + Sentiment
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    # Sentiment Analysis
    return np.array(bag)
  
def predict_class(sentence):
    bow = bagw(sentence)
    print(bow)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res)
               if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]],
                            'probability': str(r[1])})
        return return_list
    

def get_name(sentence):
    sent = nlp(sentence.title())
    return " ".join(token.text for token in sent if token.pos_ == 'PROPN')


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['label'] == tag:                
            result = random.choice(i['outputs'])
            break
    return result

def get_subject(sentence):
    sentence = nlp(sentence)
    return " ".join(token.text for token in sentence if token.dep_ == 'nsubj')
  
print("Chatbot is up!")
  
while True:
    message = input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    if ints[0]['intent'] == 'introduction response':
        name = get_name(message)
        print(name)
        res = res.replace("<name>", name)
    if ints[0]['intent'] == 'favorite':
        subject = get_subject(message)
        res = res.replace("<noun>", subject)
        
    print(res)