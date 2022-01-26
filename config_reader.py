import yaml
import logging

def read_config():
    with open('resources/config.yaml', 'r') as config_data:
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

        options_data = {}
        options_data['provider'] = opt_data['provider']
        options_data['host'] = opt_data['host']
        options_data['port'] = opt_data['port']
        options_data['user_name'] = opt_data['user_name']
        options_data['schema_name'] = opt_data['schema_name']
        config['options_data'] = options_data

    def parse_credentials():
        # credentials
        credentials = {}
        credentials['type'] = yaml_data['credentials']['provider']
        config['credentials'] = credentials

        # populate password if stored in file
        if credentials['type'].lower() == 'cred-file' and 'user_passwd' in yaml_data['storage']['options_data']:
            config['options_data']['user_passwd'] = yaml_data['options_data']['user_passwd']

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