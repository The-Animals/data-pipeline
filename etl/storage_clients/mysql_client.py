from mysql import connector
from pandas import DataFrame
from sqlalchemy import create_engine

from .utils import get_config

class MySqlClient(object):

    def __init__(self):
        config = get_config()
        self._cnx = connector.connect(
            user=config['mysql']['user'],
            password=config['mysql']['password'],
            host=config['mysql']['host'],
            database=config['mysql']['db'],
        )
        self._cnx_v2 = create_engine("mysql://{0}:{1}@{2}/{3}".format(config['mysql']['user'], config['mysql']['password'], config['mysql']['host'], config['mysql']['db'])).connect()

    def get_connection(self):
        return self._cnx

    def get_connection_v2(self):
        # user = config['mysql']['user']
        # password = config['mysql']['password']
        # host = config['mysql']['host']
        # #database = config['mysql']['db']
        #
        # engine = create_engine("mysql://{0}:{1}@{2}/{3}".format(user, password, host, database))
        # return engine.connect()
        return self._cnx_v2

    def execute_query(self, query):
        """
        Execute the query string and return a dataframe containing the queried table
        """
        cursor = self._cnx.cursor()
        cursor.execute(query)
        df = DataFrame(cursor.fetchall())
        df.columns = [d[0] for d in cursor.description]
        return df
