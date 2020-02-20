class MLA:
    def __init__(self, name):
        print(name)
        self.name = name
        self.sessions = []

    @property
    def sentences(self):
        sentences = []
        for s in self.sessions:
            sentences += s.sentences
        return sentences

    def addSession(self, session):
        self.sessions += [session]
