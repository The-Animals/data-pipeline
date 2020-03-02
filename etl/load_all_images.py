from sys import argv
from os.path import abspath
from preprocess.webscraping import get_urls, overwrite_urls
from storage_clients import MySqlClient

IMAGES_URL ='http://www.assembly.ab.ca/net/index.aspx?p=mla_report&memPhoto=True&alphaboth=True&alphaindex=True&build=y&caucus=All&conoffice=True&legoffice=True&mememail=True'

mysql_client = MySqlClient()

if __name__ == '__main__':
    if len(argv) == 2:
        IMAGES_URL = argv[1]

    print(IMAGES_URL)

    # df = get_urls(HANSARD_SESSION_URL)
    # mysql_client('documents', df)
