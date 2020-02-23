import nltk
from ..settings import config
import re

class Sentence:

    def __init__(self, text, session):
        self._text = text
        self._stopwords = config.stopwords
        self._stemmer = config.stemmer
        self._tokens = self.tokenize()
        self._length = len(self.tokens)
        self._rank = 0.0

        self._session = session
        self._mla = session.mla
        session.addSentence(self)

    @property
    def text(self):
        return self._text

    @property
    def tokens(self):
        return self._tokens

    @property
    def length(self):
        return self._length

    @property
    def rank(self):
        return self._rank

    @property
    def session(self):
        return self._session

    @property
    def mla(self):
        return self._mla

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    def tokenize(self):
        words = nltk.word_tokenize(self._text)
        validWords = []
        for word in words:
            word = word.lower()
            if word not in self._stopwords and re.search(r"^[^\W\d_]+$", word):
                word = self._stemmer.stem(word)
                validWords += [word]
        return validWords
