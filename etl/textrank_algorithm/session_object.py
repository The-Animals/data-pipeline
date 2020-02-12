class Session:

    def __init__(self, dateCode):
        self.dateCode = dateCode
        self.sentences = []

    def getDateCode(self):
        return self.dateCode

    def addSentence(self, sentence):
        self.sentences += [sentence]

    def getSentences(self):
        return self.sentences
