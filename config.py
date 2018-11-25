import configparser
import json

config = configparser.ConfigParser()
config.read('buttons.ini')

def updateSectionKeyValue(section, key, value):
    config[section][key] = json.dumps(value)
    with open('buttons.ini', 'w') as configfile:
        config.write(configfile)

def getSectionKeyValue(section, key, default):
    return json.loads(config[section].get(key, json.dumps(default)))


config.save = updateSectionKeyValue
config.load = getSectionKeyValue

