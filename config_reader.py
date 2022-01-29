import yaml
import logging
import os

def read_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/resources/config.yaml', 'r') as config_data:
        try:
            yaml_data = yaml.safe_load(config_data)

            try:
                config = parse_config_data(yaml_data)
            except Exception as e:
                print('Structure of YAML config is different from expected format')
                raise e 

            return config
        except Exception as e:
            print('Cannot read or parse config file')
            raise e

def parse_config_data(yaml_data):

    config = {}

    def parse_storage():
        opt_data = yaml_data['storage']['options_data']

        config['opdata_provider'] = opt_data['provider']
        config['opdata_host'] = opt_data['host']
        config['opdata_port'] = opt_data['port']
        config['opdata_database'] = opt_data['database_name']

    def parse_credentials():
        # credentials
        config['credentials_provider'] = yaml_data['credentials']['provider']
        if 'secret' in yaml_data['credentials']:
            config['credentials_secret'] = yaml_data['credentials']['secret']


    def parse_logging():
        config['logging_level_str'] = yaml_data['logging']['level']
        logging_level_str = config['logging_level_str'].upper()

        if logging_level_str == 'DEBUG':
            logging_level = logging.DEBUG
        elif logging_level_str == 'INFO':
            logging_level = logging.INFO
        elif logging_level_str == 'WARNING':
            logging_level = logging.WARNING
        elif logging_level_str == 'ERROR':
            logging_level = logging.ERROR
        elif logging_level_str == 'CRITICAL':
            logging_level = logging.CRITICAL
        else:
            print("Logging level not set correctly, setting to INFO")
            logging_level = logging.INFO
        
        config['logging_level'] = logging_level
    
    parse_storage()
    parse_credentials()
    parse_logging()

    return config

config_data = read_config()