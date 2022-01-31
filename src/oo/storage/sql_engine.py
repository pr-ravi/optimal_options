from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base
import os

class SqlEngine():
    def __init__(self, config) -> None:
        self.sql_metadata = MetaData()
        self.conn_str = self.__sql_get_conn_str__(config)
        self.engine = create_engine(self.conn_str)
        self.SqlBase = declarative_base(metadata = self.sql_metadata)

    def __sql_get_conn_str__(self, config):

        def get_dialect():
            dialect = ""
            if config['opdata_provider'] == 'postgres':
                dialect = "postgresql+psycopg2"
            
            return dialect

        user_name = os.environ['OO_DB_USER']
        user_pwd = os.environ['OO_DB_PWD']

        return f"{get_dialect()}://{user_name}:{user_pwd}@{config['opdata_host']}:{config['opdata_port']}/{config['opdata_database']}"