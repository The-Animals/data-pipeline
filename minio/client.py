class Minio:

    def __init__(self, address):
        self.address = address
        self.location = '../filesystem'

    def writeSpeeches(self, info):
        """Grabs legislative assembly info dictionary of the form provided by the SpeechParser class and writes each speech to minio database

        Args:
            info (dict): Info dict of the form found in SpeechParser. Can be accessed with the getInfo method
        Returns:
            N/A
        Notes:
            N/A

        """

        speakers = info['speakers']

        for speaker, speakerInfo in speakers.items():
            if self.inDatabase(speaker):
                self.writeSpeech(speaker, speakerInfo['speech'])

    def inDatabase(self, speaker):
        return True

    def writeSpeech(self, speaker, speech):
        print("Speaker is:" + speaker)
        print("Speech:\n" + speech)
        print("----------------------")

    
