class Sentence:

    def __init__(self, sentence, mla, datecode):
        self.sentence = sentence
        self.mla = mla
        self.datecode = datecode

    def getSentence(self):
        return self.sentence

    def getMla(self):
        return self.mla

    def getDatecode(self):
        return self.datecode
