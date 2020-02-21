class Session:

    def __init__(self, dateCode):
        self.dateCode = dateCode
        self.sentences = []
        self.numberOfSentences = 0

    def addSentence(self, sentence):
        self.sentences += [sentence]
        self.numberOfSentences += 1

    def getNumberOfSentences(self):
        return self.numberOfSentences
