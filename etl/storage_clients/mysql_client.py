from pandas import read_sql, DataFrame
from sqlalchemy import create_engine, Table
from sshtunnel import SSHTunnelForwarder
from .utils import get_config
from pathlib import Path


class MySqlClient(object):

    def __init__(self, db=None):
        config = get_config()
        self._sql_host = config['mysql']['host']
        self._sql_user = config['mysql']['user']
        self._sql_password = config['mysql']['password']
        self._sql_db = config['mysql']['db'] if db is None else db
        self._sql_port = int(config['mysql']['port'])

        self._ssh_host = config['ssh']['host']
        self._ssh_user = config['ssh']['user']
        self._ssh_pkey = Path(config['ssh']['pkey'])
        self._ssh_port = int(config['ssh']['port'])

    def open_connection(self): 
        self._ssh_tunnel = SSHTunnelForwarder(
            (self._ssh_host,  self._ssh_port),
            ssh_username=self._ssh_user,
            ssh_pkey=str(self._ssh_pkey),
            remote_bind_address=(self._sql_host, self._sql_port)
        )
        self._ssh_tunnel.SSH_TIMEOUT = 5.0
        self._ssh_tunnel.TUNNEL_TIMEOUT = 5.0
        self._ssh_tunnel.start()
        local_port = str(self._ssh_tunnel.local_bind_port)
        self._engine = create_engine(
            f'mysql+pymysql://{self._sql_user}:{self._sql_password}@{self._sql_host}:{local_port}/{self._sql_db}')

    def close_connection(self):
        self._engine.dispose()
        self._ssh_tunnel.stop()

    def __enter__(self):
        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def read_data(self, query: str):
        """
        Execute the query string and return a dataframe containing the queried table
        """
        return read_sql(query, self._engine)

    def execute(self, query: str):
        self._engine.execute(query)

    def append_data(self, table: Table , data: DataFrame):
        self._write_data(table, data)

    def drop_table(self, table: Table):
        table.drop(self._engine, checkfirst=True)

    def create_table(self, table: Table):
        table.create(self._engine, checkfirst=True)

    def overwrite_table(self, table: Table, data: DataFrame):
        table.drop(self._engine, checkfirst=True)
        table.create(self._engine)
        self._write_data(table, data)

    def _write_data(self, table: Table, data: DataFrame, if_exists='append', index=False):
        """
        Write the given dataframe to the database. By default, append to the table
        if it exists.
        """
        data.to_sql(table.name, self._engine, if_exists=if_exists, index=index)
