from importlib.resources import read_text
import yaml

class ConfigReader():
    
    def __init__(self, config_dir):
        self.config_dir = config_dir
    
    def read_text(self, config_name):
        with open(f'{self.config_dir}/{config_name}', 'r') as f:
            return f.read()

    def parse_yaml(self, yaml_text):
        try:
            yaml_data = yaml.safe_load(yaml_text)
            return yaml_data
        except Exception as e:
            print('Cannot parse YAML file')
            raise e

    def read_yaml(self, config_file):
        text = self.read_text(config_file)
        yaml_data = self.parse_yaml(text)
        return yaml_data