class MLA:
    def __init__(self, name):
        self.name = name
        self.session = []

    def getName(self):
        return self.name

    def addSession(self, session):
        self.session += [session]

    def getSessions(self, session):
        return self.sessions
