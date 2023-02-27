import nltk
stemmer = nltk.PorterStemmer()

def tokenize(sentence: str) -> list:
    return nltk.word_tokenize(sentence)

def split_sentences(input: str) -> list:
    return nltk.sent_tokenize(input)

def stem(word: str) -> str:
    return stemmer.stem(word)