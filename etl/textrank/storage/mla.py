class MLA:

    def __init__(self, name):
        self._name = name
        self._sessions = []
        self._sentences = []
        self._numberOfSessions = 0
        self._numberOfSentences = 0

    @property
    def name(self):
        return self._name

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

    @name.setter
    def name(self, name):
        self._name = name

    def addSession(self, session):
        self._sessions += [session]
        self._numberOfSessions += 1
        self._numberOfSentences += session.getNumberOfSentences()
