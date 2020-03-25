import requests
import re
from html import unescape


class SpeechParser:

    preprocess_replace = [
        (r'(?ms)\u202f',                 ' '),
        (r'(?ms)\x0c',                   ''),
        (r'(?ms)^Alberta Hansard \n',    ''),
        (r'(?ms)^\w+ \d+, \d+ \n',       ''),
        (r'(?ms)^\d+? \n',               ''),
        (r'(?ms)^\d{1,2}:\d{2} \n',      ''),
        (r'(?ms)\[.*?\]',                ''),
    ]

    speech_regex = r'(?ms)(^{0}):(.*?)(?=^(Mr\.|Ms|Mrs\.|The|head|Her|An Hon\.|Some Hon\.|Member)[\w. ()-]*?:)'

    postprocess_replace = [
        (r'\n',         ''),
        (r'[\s]{2,}',   ' '),
    ]

    def __init__(self, mlas: set): 
        """
        Construct a parser for speeches given the set of tokens that 
        delimit the start of a speech for an MLA. 

        Examples: 
            Ms Notley
            Member LaGrange
            Mr. Jason Nixon 

        """
        self.mlas = mlas

    def parse_speeches(self, raw_text): 
        """
        Parse out speeches that are delimited by the tokens in self.mlas.

        Return a dictionary of the {token: [speeches]}
        """
        text = self.preprocess(raw_text)
        return self.extract_speeches(text)
        
    def preprocess(self, raw_text):
        """
        Remove elements from the Hansard which make the speeches difficult 
        to parse out using regex. 
        """
        for regex, replacement in SpeechParser.preprocess_replace:
            raw_text = re.sub(regex, replacement, raw_text)
        return raw_text
        
    def extract_speeches(self, text):
        """
        Loop over all speech delimiting tokens in self.mlas and construct 
        a regex statement to grab their speech. Postprocess extracted speeches 
        and add them to a dictionary mapping {token: [speeches]}
        """
        speeches = {}
        
        for mla in self.mlas:
            regex = SpeechParser.speech_regex.format(mla)
            matches = re.findall(regex, text)
            
            for match in matches: 
                mla = match[0]
                speech = self.postprocess(match[1])
                
                if mla in speeches:
                    speeches[mla].append(speech)
                else:
                    speeches[mla] = [speech]

        return speeches
    
    def postprocess(self, speech): 
        """
        From an extracted speech, remove any additional newlines, etc. 
        """
        for regex, replacement in SpeechParser.postprocess_replace: 
            speech = re.sub(regex, replacement, speech)
        
        return speech
