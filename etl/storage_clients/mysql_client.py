
from pandas import read_sql, DataFrame
from sqlalchemy import create_engine
import pdb
from .utils import get_config

class MySqlClient(object):

    def __init__(self):
        config = get_config()
        user=config['mysql']['user']
        password=config['mysql']['password']
        host=config['mysql']['host']
        database=config['mysql']['db']
        self._cnx = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    def get_connection(self):
        return self._cnx

    def read_data(self, query: str): 
        """
        Execute the query string and return a dataframe containing the queried table
        """
        return read_sql(query, self._cnx)
        
    def write_data(self, table_name: str, data: DataFrame, schema=None, if_exists='replace'):
        """
        Write the given dataframe to the database. By default, replace the table 
        if it exists. 
        """
        data.to_sql(table_name, self._cnx, schema=schema, if_exists=if_exists)
    