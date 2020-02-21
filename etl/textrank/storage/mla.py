class MLA:
    def __init__(self, name):
        self.name = name
        self.sessions = []
        self.numberOfSessions = 0
        self.numberOfSentences = 0

    @property
    def sentences(self):
        sentences = []
        for s in self.sessions:
            sentences += s.sentences
        return sentences

    def addSession(self, session):
        self.sessions += [session]
        self.numberOfSessions += 1
        self.numberOfSentences += session.getNumberOfSentences()

    def getNumberOfSessions(self):
        return self.numberOfSessions

    def getNumberOfSentences(self):
        return self.numberOfSentences
