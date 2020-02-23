class Session:

    def __init__(self, dateCode):
        self._dateCode = dateCode
        self._sentences = []
        self._numberOfSentences = 0

    @property
    def dateCode(self):
        return self._dateCode

    @property
    def sentences(self):
        return self._sentences

    @property
    def numberOfSentences(self):
        return self._numberOfSentences

    def getSentence(self, sentence):
        for s in self._sentences:
            if s.text == sentence:
                return s
        return None

    def addSentence(self, sentence):
        self._sentences += [sentence]
        self._numberOfSentences += 1
