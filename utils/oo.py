import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_actions import DbActions
import arguments 
import logging
import config_reader

config = config_reader.read_config()
logging.basicConfig(level=config['logging_level'], format='%(levelname)s %(name)s: %(funcName)s %(message)s')

args = arguments.get_arguments()

env = {
    'args': args,
    'config': config
}

if args.db_cmd:
    DbActions().process(args.db_cmd, env)
