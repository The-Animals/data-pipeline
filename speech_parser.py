import requests
import re

class SpeechParser:

    def __init__(self, url):
        self.source = None
        self.text = None
        self.lines = None
        self.info = {}

        self.setSourceHTML(url)
        self.parseData()


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

        text = re.sub(r'<[ \v\t\S]*>', '', text) # remove all left over HTML context
        text = text[text.find('\n') + 1:] # TODO: Implementation leaves one line of HTML context at the beginning. Could not figure out how to work around it

        text = text.replace('\n', '') # remove new line needed for HTML removal
        text = text.replace('\r', '\n') # change all returns to new line

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
        #self.getInfo()

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

# with open("urls.txt", "r") as f:
#     urls = f.read().splitlines()
#
# for url in urls:
#     s = SpeechParser(url)
#     print(s.getInfo())
