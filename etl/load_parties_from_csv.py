from pkgutil import get_data
from pandas import read_csv
from io import StringIO

from storage_clients import MySqlClient, DbSchema

"""
load MLA data from data/parties.csv
"""


def load_parties():
    table = DbSchema.parties

    print('reading party data from csv')
    data = StringIO(str(get_data('data', 'parties.csv').decode('utf-8')))
    df = read_csv(data)

    with MySqlClient() as mysql_client:
        print('writing party data to database')
        mysql_client.overwrite_table(table, df)


if __name__ == '__main__':
    load_parties()
