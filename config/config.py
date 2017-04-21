import ConfigParser

CONFIG_FILE_NAME="config/config.ini"

Config = ConfigParser.ConfigParser()
Config.read(CONFIG_FILE_NAME)


def default_shard_count():
    return int(Config.get(section="Counter", option="DEFAULT_SHARD_COUNT"))

def shard_key_template():
    return Config.get(section="Counter", option="SHARD_KEY_TEMPLATE")

def page_key_template():
    return Config.get(section="Page", option="PAGE_KEY_TEMPLATE")

def page_max_count():
    return int(Config.get(section="Page", option="MAX_COUNT"))

def page_total_key_template():
    return Config.get(section="Page", option="TOTAL_KEY_TEMPLATE")

