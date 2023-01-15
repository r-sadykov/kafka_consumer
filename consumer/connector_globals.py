from configparser import ConfigParser
from connector_logger import ConsoleStats


def __init__():
    global users
    users = []
    global config_parser
    config_parser = ConfigParser()
    global prev_users
    prev_users = []
    global stats
    stats = ConsoleStats()
