import nltk
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import pkgutil

import re

# def get_stop_words():
#     stopwords_data = pkgutil.get_data("sumy", "data/stopwords/english.txt")
#     return frozenset(w.rstrip() for w in str(stopwords_data).splitlines() if w)

class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence
        self.stopwords = frozenset(stopwords.words('english'))
        #self.stopwords = get_stop_words()
        self.stemmer = EnglishStemmer()
        self.tokens = self.tokenize()
        self.length = len(self.tokens)
        self.rank = 0.0

    def tokenize(self):
        words = nltk.word_tokenize(self.sentence)
        validWords = []
        for word in words:
            word = word.lower()
            if word not in self.stopwords and re.search(r"^[^\W\d_]+$", word):
                word = self.stemmer.stem(word)
                validWords += [word]
        return validWords

    def getString(self):
        return self.sentence

    def getTokens(self):
        return self.tokens

    def getLength(self):
        return self.length

    def setRank(self, rank):
        self.rank = rank

    def getRank(self):
        return self.rank
