import configparser
import os

class ConfigWriter:
    def __init__(self):
        self.configParser = configparser.RawConfigParser()
        self.configFilePath = os.path.join(os.path.dirname(__file__), '../config.cfg')
        self.configParser.read(self.configFilePath)

