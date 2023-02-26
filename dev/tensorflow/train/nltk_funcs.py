import nltk
stemmer = nltk.PorterStemmer()

def tokenize(sentence: str) -> list:
    return nltk.word_tokenize(sentence)

def stem(word: str) -> str:
    return stemmer.stem(word)