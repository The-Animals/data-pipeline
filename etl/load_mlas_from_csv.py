from pkgutil import get_data
from pandas import read_csv
from io import StringIO

from storage_clients import MySqlClient, DbSchema

"""
load MLA data from data/mlas.csv
"""


def load_mlas(): 
    table = DbSchema.mlas

    print('reading mla data from csv')
    data = StringIO(str(get_data('data', 'mlas.csv').decode('utf-8')))
    df = read_csv(data)
    
    with MySqlClient() as mysql_client:
        print('writing mla data to database')
        mysql_client.overwrite_table(table, df)


if __name__ == '__main__':
    load_mlas()
