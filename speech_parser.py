import requests

class SpeechParser:

    def __init__(self, url):
        self.source = None

        self.setSourceHTML(url)


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

# s = SpeechParser("https://www.assembly.ab.ca/Documents/isysquery/0b24aeb4-4082-4331-8934-302c92e0950b/1/doc/")
#
# with open("test.txt", "w") as f:
#     source = s.getSourceHTML()
#     for l in source:
#         f.write(l)
