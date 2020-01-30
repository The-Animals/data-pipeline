import requests
import re

class SpeechParser:

    def __init__(self, url):
        self.source = None
        self.text = None
        self.info = {}

        self.setSourceHTML(url)
        self.parseText()


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
        self.source = r.content


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
        """Converts source html to natural text, removing any unwanted components

        Args:
            N/A
        Returns:
            N/A
        Notes:
            May need to be changed if HTML structure changes across documents

        """
        text = self.source
        text = text.replace('\n', '') # remove all new line as HTML new line does not represent text new line
        text = text.replace('<br />', '\n') # replace all HTML breaks with new line
        text = re.sub(r'<[ \v\t\S]*>', '', text) # remove all left over HTML context

        self.text = text[text.find('\n') + 1:] # TODO: Implementation leaves one line of HTML context at the beginning. Could not figure out how to work around it


    def parseText(self):
        """Parses text stored in the HTML into a dict response structure to be passed to blob storage.

        Args:
            N/A
        Returns:
            N/A

        """
        self.HTMLToText()

    def parseSpeeches(self):
        pass

    def getInfo(self):
        return self.info

s = SpeechParser('https://www.assembly.ab.ca/Documents/isysquery/0b24aeb4-4082-4331-8934-302c92e0950b/1/doc/')
with open('test2.txt', 'w') as f:
    f.write(s.getSourceText())
