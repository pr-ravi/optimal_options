import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .sql_engine import SqlEngine
import config_reader

sql_env = SqlEngine(config_reader.config_data)
