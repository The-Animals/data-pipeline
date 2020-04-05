from ..settings import config
import re
import nltk

class Sentence:

    def __init__(self, text, session=None, id=None):
        self._text = text
        self._id = id
        self._stopwords = config.stopwords
        self._stemmer = config.stemmer
        self._wordPattern = config.wordPattern
        self._tokens = self.tokenize()
        self._length = len(self.tokens)
        self._rank = 0

        self._session = session
        self._mla = None
        if session:
            self._mla = session.mla
            session.addSentence(self)

    @property
    def text(self):
        return self._text

    @property
    def id(self):
        return self._id

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
    def secondRank(self):
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
            if word not in self._stopwords and re.search(r"{0}".format(self._wordPattern), word):
                word = self._stemmer.stem(word)
                validWords += [word]
        return validWords
