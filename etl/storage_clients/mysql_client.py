from mysql import connector 
from pandas import DataFrame

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

    def get_connection(self):
        return self._cnx

    def execute_query(self, query): 
        """
        Execute the query string and return a dataframe containing the queried table
        """
        cursor = self._cnx.cursor()
        cursor.execute(query)
        df = DataFrame(cursor.fetchall())
        df.columns = [d[0] for d in cursor.description]
        return df
