class MLA:

    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._sessions = []
        self._sentences = []
        self._numberOfSessions = 0
        self._numberOfSentences = 0

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def sentences(self):
        sentences = []
        for s in self._sessions:
            sentences += s.sentences
        return sentences

    @property
    def sessions(self):
        return self._sessions

    @property
    def numberOfSessions(self):
        return self._numberOfSessions

    @property
    def numberOfSentences(self):
        return self._numberOfSentences

    @numberOfSentences.setter
    def numberOfSentences(self, number):
        self._numberOfSentences = number

    def getSession(self, dateCode):
        for s in self._sessions:
            if s.dateCode == dateCode:
                return s
        return None

    def getSentence(self, sentence):
        for s in self.sentences:
            if s.text == sentence:
                return
        return None

    def addSession(self, session):
        self._sessions += [session]
        self._numberOfSessions += 1
        self._numberOfSentences += session.numberOfSentences

    def addSentence(self, dateCode, sentence):
        session = getSession(dateCode)
        session.addSentence(sentence)
