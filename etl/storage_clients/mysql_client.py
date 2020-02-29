from pandas import read_sql, DataFrame
from sqlalchemy import create_engine, Table
from sshtunnel import SSHTunnelForwarder
from .utils import get_config
from pathlib import Path


class MySqlClient(object):

    def __init__(self):
        config = get_config()
        self._sql_host = config['mysql']['host']
        self._sql_user = config['mysql']['user']
        self._sql_password = config['mysql']['password']
        self._sql_db = config['mysql']['db']
        self._sql_port = int(config['mysql']['port'])

        self._ssh_host = config['ssh']['host']
        self._ssh_user = config['ssh']['user']
        self._ssh_pkey = Path(config['ssh']['pkey'])
        self._ssh_port = int(config['ssh']['port'])

    def __enter__(self):
        self._ssh_tunnel = SSHTunnelForwarder(
            (self._ssh_host,  self._ssh_port),
            ssh_username=self._ssh_user,
            ssh_pkey=str(self._ssh_pkey),
            remote_bind_address=(self._sql_host, self._sql_port)
        )
        self._ssh_tunnel.start()
        local_port = str(self._ssh_tunnel.local_bind_port)
        self._engine = create_engine(
            f'mysql+pymysql://{self._sql_user}:{self._sql_password}@{self._sql_host}:{local_port}/{self._sql_db}')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._engine.dispose()
        self._ssh_tunnel.close()

    def read_data(self, query: str):
        """
        Execute the query string and return a dataframe containing the queried table
        """
        return read_sql(query, self._engine)

    def execute(self, query: str):
        self._engine.execute(query)

    def append_data(self, table: Table , data: DataFrame):
        self._write_data(table.name, data)

    def drop_table(self, table: Table):
        table.drop(self._engine, checkfirst=True)

    def create_table(self, table: Table):
        table.create(self._engine, checkfirst=True)

    def overwrite_table(self, table: Table, data: DataFrame):
        table.drop(self._engine, checkfirst=True)
        table.create(self._engine)
        self._write_data(table.name, data)

    def _write_data(self, table_name: str, data: DataFrame, if_exists='append', index=False):
        """
        Write the given dataframe to the database. By default, append to the table
        if it exists.
        """
        data.to_sql(table_name, self._engine, if_exists=if_exists, index=index)
