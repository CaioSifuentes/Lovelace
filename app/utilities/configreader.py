import os
from dotenv import load_dotenv
import json

dev_mode = True

class ConfigReader:
    @staticmethod
    def get_mode():
        return dev_mode

    @staticmethod
    def get_token():
        env_file = 'dev.env' if dev_mode else 'prod.env'
        load_dotenv(env_file)
        return os.getenv("TOKEN")
    
    @staticmethod
    def get_config():
        config_file = './app/config-dev.json' if dev_mode else './app/config.json'
        with open(config_file, 'r', encoding='utf-8') as config:
            return json.load(config)
