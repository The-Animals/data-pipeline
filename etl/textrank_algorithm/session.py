class Session:

    def __init__(self, dateCode):
        self.dateCode = dateCode
        self.sentences = []

    def addSentence(self, sentence):
        self.sentences += [sentence]
