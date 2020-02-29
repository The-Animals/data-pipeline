from sys import argv
from os.path import abspath
from preprocess.webscraping import get_urls, overwrite_urls
from storage_clients import MySqlClient

HANSARD_SESSION_URL ='https://www.assembly.ab.ca/net/index.aspx?p=han&section=doc&fid=1'

mysql_client = MySqlClient()

if __name__ == '__main__':
    if len(argv) == 2:
        HANSARD_SESSION_URL = argv[1]

    df = get_urls(HANSARD_SESSION_URL)
    mysql_client('documents', df)
