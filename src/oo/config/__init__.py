from .config_reader import ConfigReader
from .main_config_parser import MainConfigParser
import os 

config_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
config_dir = config_dir + os.path.sep + "resources"

reader = ConfigReader(config_dir)

__main_config__parser__ = MainConfigParser(reader)
__main_config__parser__.parse()

main_config = __main_config__parser__.config

#print(main_config)