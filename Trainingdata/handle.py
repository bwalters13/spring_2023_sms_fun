import json
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



with open('test.json', 'r') as f:
  data = json.load(f)
humanInput = []
botOutput = []
for entry in data:
    for list in entry["dialog"]:
        if list["sender_class"] == "Bot":
            botOutput.append(list["text"])
        elif list["sender_class"] == "Human":
            humanInput.append(list["text"])

#print(botOutput)
#print(humanInput)
postiveResponses = []
def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
     
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    # print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
        postiveResponses.append(sentence)
 
    # elif sentiment_dict['compound'] <= - 0.05 :
    #     print("Negative")
 
    # else :
    #     print("Neutral")

for evrStr in botOutput:
    sentiment_scores(evrStr)

print(postiveResponses)