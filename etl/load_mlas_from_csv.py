from pkgutil import get_data
from pandas import read_csv, Dataframe
from io import StringIO
from tests.assertions import assert_mla_table_format

from storage_clients import MySqlClient, DbSchema

"""
load MLA data from data/mlas.csv
"""

n_mlas = 87


def assert_mla_table_format(df: Dataframe):
    counts = df.count()
    assert counts.FirstName == n_mlas
    assert counts.LastName == n_mlas
    assert counts.RidingNumber == n_mlas
    assert counts.RidingName == n_mlas
    assert counts.HansardName == n_mlas
    assert counts.HansardName == n_mlas


def load_mlas():
    table = DbSchema.mlas

    print('reading mla data from csv')
    data = StringIO(str(get_data('data', 'mlas.csv').decode('utf-8')))
    df = read_csv(data)

    assert_mla_table_format(df)

    with MySqlClient() as mysql_client:
        print('writing mla data to database')
        mysql_client.overwrite_table(table, df)


if __name__ == '__main__':
    load_mlas()
