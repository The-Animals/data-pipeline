from pkgutil import get_data 
from configparser import ConfigParser
from io import StringIO

def get_config():
    """
    Return configuration which should be stored at etl/config.ini
    """
    config = ConfigParser()
    raw_config = get_data(__package__, 'config.ini').decode('utf-8')
    config.read_file(StringIO(raw_config))
    return config