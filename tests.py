from speech_parser import SpeechParser
import unittest

class TestSpeechParser(unittest.TestCase):

    def setUp(self):
        with open("urls.txt", "r") as f:
            self.urls = f.read().splitlines()

    def test_bad_urls(self):
        ''' Tests invalid urls and ensures value error is raised'''
        self.assertRaises(ValueError, SpeechParser, 'The Animals')
        self.assertRaises(ValueError, SpeechParser, 2)
        self.assertRaises(ValueError, SpeechParser, True)
        self.assertRaises(ValueError, SpeechParser, None)

    def test_good_urls(self):
        ''' Tests valid urls and ensures value error is raised'''
        for url in self.urls:
            s = SpeechParser(url)
            self.assertTrue(type(s.getSourceHTML()) == str)

    def test_metadata(self):
        ''' Tests metadata to ensure data is valid'''
        for url in self.urls:
            s = SpeechParser(url)
            metadata = s.getInfo()['metadata']
            self.assertTrue(metadata['province'] == 'Alberta')
            self.assertTrue(metadata['assembly'] == '30')
            self.assertTrue(metadata['date']['month'] in ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
            self.assertTrue(metadata['date']['weekday'] in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
            self.assertTrue(metadata['date']['time'] in ('morning', 'afternoon', 'evening'))
            self.assertTrue(2010 < int(metadata['date']['year']) < 2021)
            self.assertTrue(0 < int(metadata['date']['day']) < 32)


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
