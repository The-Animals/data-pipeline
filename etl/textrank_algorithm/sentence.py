from textrank_algorithm import Tokenizer

class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokenizer = Tokenizer("english")

    def getWords(self):
        return self.tokenizer.to_words(self.sentence)
