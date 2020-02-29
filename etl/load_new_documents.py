from sys import argv
from os.path import abspath
from preprocess.webscraping import get_urls, overwrite_urls

from storage_clients import MySqlClient, DbSchema

HANSARD_SESSION_URL ='https://www.assembly.ab.ca/net/index.aspx?p=han&section=doc&fid=1'

"""
Scrape Hansard website for document urls and meta data to be stored 
in the database
"""


def load_new_documents(): 
    table = DbSchema.documents

    with MySqlClient() as mysql_client:
        print('reading previously seen documents from database')
        prev_docs = mysql_client.read_data('documents')

    docs = get_urls(HANSARD_SESSION_URL)
    new_date_codes = list(set(docs['DateCode']) - set(prev_docs['DateCode']))
    new_docs = docs.loc[docs['DateCode'].isin(new_date_codes)]

    with MySqlClient() as mysql_client:
        print('writing new documents to database')
        mysql_client.append_data(table, new_docs)



if __name__ == '__main__':
    load_new_documents()
