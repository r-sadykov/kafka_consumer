from collections import OrderedDict
import json
from consumer.connector_filters import *
from consumer.connector_library_classes import *
from consumer.connector_logger import print_errorInfo
import consumer.connector_globals as globals


def getPoll(file):
    str = ''
    list = []
    with open(file, mode='r', encoding='utf-8-sig') as f:
        originalPosition = f.tell()
        eofPosition = f.seek(0, 2)
        f.seek(originalPosition)
        while (f.tell() != eofPosition):
            line = f.readline().strip()
            if line == '':
                list.append(str)
                str = ''
                continue
            str += line.rstrip('\n')
    return list


def isObject(item):
    check_str = item[:20]
    if "guid" in check_str:
        return "guid"
    elif "isUFLog" in check_str:
        return "isUFLog"
    elif "channel" in check_str:
        return "channel"
    elif "data" in check_str:
        return "data"
    elif "actualTimestamp" in check_str:
        return "actualTimestamp"
    elif "officeCode" in check_str:
        return "officeCode"
    elif "gpbGuid" in check_str:
        return "gpbGuid"


def toDictionary(str):
    try:
        dict = json.loads(str, object_pairs_hook=OrderedDict)
        return dict
    except Exception as e:
        print_errorInfo(e)
        pass


def getNboLog(item):
    if "gpbGuid" == isObject(item.message):
        dic = toDictionary(item.message)
        try:
            gpb = nboWithResponseLog_fromDict(dic)
            return gpb
        except:
            return None


def getNboResponseLog(item):
    return getNboLog(item)


def isLoginExist(item):
    if isinstance(item, ClientLog):
        if item.login != "" and item.login != None:
            return True
        return False
    if isinstance(item, NboWithResponseLog):
        if item.user_login != "" and item.user_login != None:
            return True
        return False
    return False


def isNboLog(item):
    if isinstance(item, KafkaLog):
        if item.app_name == globals.config_parser['filters']['nbo_log_app_name'] and globals.config_parser['filters']['nbo_log_logger_name'] in item.logger_name:
            return True
        return False
    return False


def isNboResponseLog(item):
    if isinstance(item, KafkaLog):
        if item.app_name == globals.config_parser['filters']['nbo_response_log_app_name'] and globals.config_parser['filters']['nbo_response_log_logger_name'] in item.logger_name:
            return True
        return False
    return False


def getClientLog(item):
    if "channel" == isObject(item.message):
        if 'meta' in item.message and 'bffHttpMethod' in item.message:
            return None
        dic = toDictionary(item.message)
        try:
            clientLog = clientLog_fromDict(dic)
            return clientLog
        except:
            return None
    return None


def value_toKafkaObject(item):
    if isinstance(item, KafkaLog):
        return item
    elif isinstance(item, dict):
        return kafkaLog_fromDict(item)
    elif isinstance(item, str):
        return kafkaLog_fromDict(toDictionary(item))
    else:
        print("... none object")
        return None


def isClientLog(item):
    if isinstance(item, KafkaLog):
        if item.app_name == globals.config_parser['filters']['client_log_app_name'] and globals.config_parser['filters']['client_log_logger_name'] in item.logger_name:
            return True
        return False
    return False
