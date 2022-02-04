import logging

class MainConfigParser():

    def __init__(self, config_reader) -> None:
        self.__config_reader__ = config_reader
        self.config = {}

    def parse(self):
        text = self.__config_reader__.read_text('config.yaml')
        self.yaml_data = self.__config_reader__.parse_yaml(text)

        try:
            self.parse_app()
            self.parse_storage()
            self.parse_credentials()
            self.parse_logging()
        except Exception as e:
            print('Cannot parse config.yaml, structure error') 
            raise e 

    def parse_app(self):
        opt_app = self.yaml_data['app']

        self.config['app_name'] = opt_app['name']
        self.config['app_version'] = opt_app['version']

    def parse_storage(self):
        opt_data = self.yaml_data['storage']['options_data']

        self.config['opdata_provider'] = opt_data['provider']
        self.config['opdata_host'] = opt_data['host']
        self.config['opdata_port'] = opt_data['port']
        self.config['opdata_database'] = opt_data['database_name']   

    def parse_credentials(self):
        # credentials
        self.config['credentials_provider'] = self.yaml_data['credentials']['provider']
        if 'secret' in self.yaml_data['credentials']:
            self.config['credentials_secret'] = self.yaml_data['credentials']['secret']

    def parse_logging(self):
        self.config['logging_level_str'] = self.yaml_data['logging']['level']
        logging_level_str = self.config['logging_level_str'].upper()

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
        
        self.config['logging_level'] = logging_level