from speech_parser import SpeechParser
import unittest

class TestSpeechParser(unittest.TestCase):

    def setUp(self):
        self.url = "https://www.assembly.ab.ca/Documents/isysquery/0b24aeb4-4082-4331-8934-302c92e0950b/1/doc/"
        self.parser = SpeechParser(self.url)

    def test_bad_url(self):
        ''' Tests invalid urls and ensures value error is raised'''
        self.assertRaises(ValueError, self.parser.setSourceHTML, 'The Animals')
        self.assertRaises(ValueError, self.parser.setSourceHTML, 2)
        self.assertRaises(ValueError, self.parser.setSourceHTML, True)
        self.assertRaises(ValueError, self.parser.setSourceHTML, None)

    def test_good_url(self):
        ''' Tests invalid urls and ensures value error is raised'''
        self.assertTrue(type(self.parser.getSourceHTML()) == str)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
