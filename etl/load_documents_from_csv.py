from pkgutil import get_data
from pandas import read_csv
from io import StringIO

from storage_clients import MySqlClient, DbSchema

"""
load document data from data/documents.csv
"""

def load_documents():
    table = DbSchema.documents

    print('reading document data from csv')
    data = StringIO(str(get_data('data', 'documents.csv').decode('utf-8')))
    df = read_csv(data)
    
    with MySqlClient() as mysql_client:
        print('writing document data to database')
        mysql_client.overwrite_table(table, df)


if __name__ == '__main__':
    load_documents()
