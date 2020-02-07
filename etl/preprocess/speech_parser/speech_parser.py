import requests
import re
from html import unescape

class SpeechParser:

    def __init__(self, url, names):
        self.source = None
        self.text = None
        self.lines = None
        self.info = {}
        self.names = set(names)

        self.setSourceHTML(url)

    def getAssembly(self):
        """Grabs legislative assembly metadata from natural text stored in object text variable. HTMLToText must be invoked successfully in order for this function to work valid.

        Args:
            N/A
        Returns:
            String: Assembly found in raw text
        Notes:
            May need to be changed if HTML structure changes across documents

        """

        try:
            line = self.lines[3] # Set line of info
            return re.findall(r'The (\d+)th Legislature', line)[0]
        except:
            raise ValueError("Could not extract legislative assembly data from text")

    def getDate(self):
        """Grabs legislative assembly metadata from natural text stored in object text variable. HTMLToText must be invoked successfully in order for this function to work valid.

        Args:
            N/A
        Returns:
            String: Assembly found in raw text
        Notes:
            May need to be changed if HTML structure changes across documents

        """
        date = {}

        try:
            line = self.lines[7] # Set line of info
            dateInfo = re.findall(r'(\w+) (\w+), (\w+) (\d+), (\d+)', line)[0] # Extracts info from line of the form Wednesday afternoon, May 22, 2019

            date["weekday"] = dateInfo[0]
            date["time"] = dateInfo[1]
            date["month"] = dateInfo[2]
            date["day"] = dateInfo[3]
            date["year"] = dateInfo[4]

            return date
        except:
            raise ValueError("Could not extract legislative assembly data from text")

    def getInfo(self):
        """Gets all information (metadata, politician, and speech) from object, which is contained in a dictionary

        Args:
            N/A
        Returns:
            Dict: Dict of information

        """

        return self.info

    def getProvince(self):
        """Grabs province metadata from natural text stored in object text variable. HTMLToText must be invoked successfully in order for this function to work valid.

        Args:
            N/A
        Returns:
            String: Province found in raw text
        Notes:
            May need to be changed if HTML structure changes across documents

        """

        try:
            line = self.lines[1] # Set line of info
            return re.findall(r'Province of (\w+)', line)[0]
        except:
            raise ValueError("Could not extract province data from text")

    def getSourceHTML(self):
        """Gets the source HTML stored in object and returns as a string. setSourceHTML must be invoked successfully prior to this, otherwise None type is returned.

        Args:
            N/A
        Returns:
            String: Returns raw HTML string received from the URL.
            None: Returns none type upon failed retrival of HTML data.
        Notes:
            May not be needed in actual implementation (done in another object maybe??)

        """

        return self.source

    def getSourceText(self):
        """Gets the source text (converted from HTML) stored in object and returns as a string. The object must have been initialized properly for this to return a valid value.

        Args:
            N/A
        Returns:
            String: Returns raw text string converted from HTML URL.
            None: Returns none type upon failed retrieval of text.

        """

        return self.text

    def HTMLToText(self):
        """Converts source html to natural text, removing any unwanted components. Stores raw text in object text variable, and array of lines in object lines variable

        Args:
            N/A
        Returns:
            N/A
        Notes:
            May need to be changed if HTML structure changes across documents

        """
        text = self.source

        text = text.replace('\n', '') # remove all new line as HTML new line does not represent text new line
        text = text.replace('<br />', '\n') # replace all HTML breaks with new line (needed to remove HTML data)

        text = re.sub(r'<[\/ \v\t\S]+?>', '', text) # remove all left over HTML context

        text = text[text.find('\n') + 1:] # TODO: Implementation leaves one line of HTML context at the beginning. Could not figure out how to work around it

        text = text.replace('\n', '') # remove new line needed for HTML removal
        text = text.replace('\r', '\n') # change all returns to new line

        text = re.sub(r'[\x96]', '-', text) # python cannot decode \x96 in iso-8859-1

        self.text = text
        self.lines = self.text.splitlines()

    def parseData(self):
        """Parses data stored in the HTML into a dict response structure to be passed to blob storage.

        Args:
            N/A
        Returns:
            N/A

        """
        self.HTMLToText()
        self.setMetaData()
        self.setSpeeches()

    def setMetaData(self):
        """Grabs metadata from natural text stored in object text variable. HTMLToText must be invoked successfully in order for this function to work valid.

        Args:
            N/A
        Returns:
            N/A
        Notes:
            May need to be changed if HTML structure changes across documents

        """
        metadata = {}

        # Set info
        metadata['province'] = self.getProvince()
        metadata['assembly'] = self.getAssembly()
        metadata['date'] = self.getDate()

        self.info['metadata'] = metadata

    def setSourceHTML(self, url):
        """Sets the source of the Hansard document and retrieves the raw HTML text using the requests library, storing it in the objects source variable.

        Args:
            url (String): URL to get HTML information
        Returns:
            No value is returned. ValueError is raised upon an invalid request, with status code being printed.
        Notes:
            May not be needed in actual implementation (done in another object maybe??)

        """

        try:
            r = requests.get(url)
        except:
            raise ValueError("Invalid URL {0} used, could not submit request".format(url))
            return

        if r.status_code != 200:
            raise ValueError("Invalid URL {0} used, received status code {1}".format(url, r.status_code))
        self.source = r.content.decode('iso-8859-1')

    def setSpeeches(self):
        """Sets speaker and speach information in object info dictionary by parsing through raw text. HTMLTOText must be invoked successfully with a standard Hansard document matching the regex rules found in order for this to work properly.

        Args:
            N/A
        Returns:
            N/A
        Notes:
            Highly specific to document structure. May need changing as more URLs are tested for injestion.

        """

        speakers = {}

        # Define portion of text to search
        try:
            beginning = re.search(r'Title: \w+, \w+ \d+, \d+ \d+:\d+ (a|p).m.\n\d+(:\d+)? (a|p).m. \w+, \w+ \d+, \d+', self.text).group(0) # Right before speeches
            end = re.search(r'Table of Contents\n', self.text).group(0) # Right after speeches
            speechText = self.text.split(beginning)[1].split(end)[0]
        except:
            raise ValueError("Failed to find range of speech text in document based on Hansard document structure. Please ensure URL points to a Hansard document.")

        # Remove unwanted Hansard information
        speechText = re.sub(r'\n\n\d+ Alberta Hansard \w+ \d+, \d+\n\n', '', speechText) # removes Hansard information (1 of 2)
        speechText = re.sub(r'\n\n\w+ \d+, \d+ Alberta Hansard \d\n\n', '', speechText) # removes Hansard information (2 of 2)

        # Split each speech into it's own portion. Each will be seperated by \n\n at this point
        for section in speechText.split('\n\n'):
            # If the start of someone speaking (there may still be some stray lines in here that aren't speeches (times, headings, and information))
            if re.match(r'^[A-Za-z\.\-() ]+:', section):
                
                speaker = section.split(':')[0] # remove colon at end of speaker name, now stores name
                last_name = speaker.split(' ')[-1]
                if last_name not in self.names:
                    continue
                try: 
                    speech = section.split(speaker)[1][2:] # add beginning of speech after colon (2 spaces after name ends)
                    speech = speech.replace('\n', ' ') # removes line breaks in speech
                    if last_name not in speakers:
                        speakers[last_name] = list()
                    speakers[last_name].append(speech)
                except:
                    raise ValueError("Failed to extract data for speaker. Please ensure URL points to a Hansard document.")

        self.info['speakers'] = speakers
