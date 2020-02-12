class MLA:
    def __init__(self, name):
        self.name = name
        self.sessions = []

    def getName(self):
        return self.name

    def addSession(self, session):
        self.sessions += [session]

    def getSessions(self):
        return self.sessions
