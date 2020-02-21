import nltk
import re

class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence

    def getWords(self):
        words = nltk.word_tokenize(self.sentence)
        validWords = ()
        for word in words:
            if re.search(r"^[^\W\d_]+$", word):
                validWords += (word,)
        return validWords
