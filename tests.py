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

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
