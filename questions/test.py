import os
import nltk
import string

corpus = {
    "A":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
    "B":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
    "C":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
    "B":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
    "E":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
    "AF":["APPLE", "APPLE", "APPLE", "Pineapple", "banana", "banana"],
}

document = "When is Python 3.0 released?"

# to perform tokenization
words = nltk.word_tokenize(document.lower())


# Filter out punctuation and stopwords
punctuation = set(string.punctuation)
stopwords = set(nltk.corpus.stopwords.words("english"))


for word in words.copy():
    print (word)
    words.remove(word)