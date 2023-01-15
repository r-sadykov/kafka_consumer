import datetime
import logging
import logging.handlers as handlers
import os
from typing import Any
from requests import Response
from consumer.connector_library_classes import *

logging.basicConfig(level=logging.INFO)


class ErrorLogger:
    def __init__(self) -> None:
        self.error_logger = logging.getLogger("error")
        self.error_logger.setLevel(logging.ERROR)
        self.error_formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: PID_%(process)d :: %(funcName)s :: %(thread)d :: %(message)s')
        self.log_path = get_logFolderPath()
        self.logHandler = handlers.TimedRotatingFileHandler(
            os.path.join(self.log_path, "error.log"),
            when='D',
            interval=1,
            backupCount=30)
        self.logHandler.setLevel(logging.ERROR)
        self.logHandler.setFormatter(self.error_formatter)
        self.logHandler.suffix = "%Y%m%d"
        self.logHandler.namer = get_filename
        self.error_logger.addHandler(self.logHandler)


class SourceFilter(logging.Filter):
    def filter(self, record):
        record.timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        record.source = record.source
        record.user = record.user
        record.key = record.key
        record.value = record.value
        return True


class SourceLogger:
    def __init__(self) -> None:
        self.source_logger = logging.getLogger("source")
        self.source_logger.setLevel(logging.INFO)
        self.source_logger.addFilter(SourceFilter())
        self.source_formatter = logging.Formatter(
            '{"timestamp":"%(timestamp)s","levelname":"%(levelname)s","thread":"%(thread)d","message":"%(message)s","source":"%(source)s","user":"%(user)s","key":"%(key)s","value":%(value)s}')
        self.log_path = get_logFolderPath()
        self.logHandler = handlers.RotatingFileHandler(
            os.path.join(self.log_path, "source.log"),
            maxBytes=12582912,
            backupCount=100)
        self.logHandler.setLevel(logging.INFO)
        self.logHandler.setFormatter(self.source_formatter)
        self.logHandler.namer = get_filename
        self.source_logger.addHandler(self.logHandler)


class HttpFilter(logging.Filter):
    def filter(self, record):
        record.timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        record.http_status = record.http_status
        record.http_reason = record.http_reason
        record.http_method = record.http_method
        record.http_uri = record.http_uri
        record.http_headers = record.http_headers
        record.http_response = record.http_response
        record.user = record.user
        record.value = record.value
        return True


class HttpLogger:
    def __init__(self) -> None:
        self.http_logger = logging.getLogger("http")
        self.http_logger.setLevel(logging.INFO)
        self.http_logger.addFilter(HttpFilter())
        self.http_formatter = logging.Formatter(
            '{"timestamp":"%(timestamp)s", "level":"%(levelname)s", "thread": "%(thread)d", "errorMessage":"%(message)s", "http_status": "%(http_status)s", "http_reason": "%(http_reason)s", "http_method": "%(http_method)s", "http_uri": "%(http_uri)s", "http_headers": "%(http_headers)s", "http_response": "%(http_response)s", "user: %(user)s", "value": %(value)s}')
        self.log_path = get_logFolderPath()
        self.logHandler = handlers.RotatingFileHandler(
            os.path.join(self.log_path, "http_response.log"),
            maxBytes=12582912,
            backupCount=100)
        self.logHandler.setLevel(logging.INFO)
        self.logHandler.setFormatter(self.http_formatter)
        self.logHandler.namer = get_filename
        self.http_logger.addHandler(self.logHandler)


def get_logFolderPath() -> str:
    dir_path = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def get_filename(filename):
    # Get logs directory
    log_directory = os.path.split(filename)[0]
    # Get file extension (also it's a suffix's value (i.e. ".20181231")) without dot
    file_arr = os.path.splitext(filename)
    date = file_arr[1][1:]
    cur_index = 0
    if type(int(date)) == int:
        cur_index = int(date)
    rest_path = file_arr[0]
    file_source = os.path.split(rest_path)[1]
    text_arr = file_source.split(".")
    file_name = text_arr[0]
    # Create new file name
    filename = os.path.join(log_directory, file_name+"."+date)
    # I don't want to add index if only one log file will exists for date
    if not os.path.exists('{}.log'.format(filename)):
        return '{}.log'.format(filename)
    # Create new file name with index
    index = 0
    f = None
    if cur_index == index:
        cur_index += 1
        f = '{}.log'.format(filename, cur_index)
    else:
        f = '{}.{}.log'.format(filename, index)
        while os.path.exists(f):
            index += 1
            f = '{}.{}.log'.format(filename, index)
    return f


errorLogger = ErrorLogger()
sourceLogger = SourceLogger()
httpLogger = HttpLogger()


def print_errorInfo(msg):
    errorLogger.error_logger.error(msg)


def print_rawText(item: Any, suffix: str, source: str, msg: str):
    dir_path = get_logFolderPath()
    log_path = os.path.join(dir_path, datetime.now().strftime(
        "%Y_%m_%d")+"_"+source+"_"+suffix+".txt")
    message = ""
    if msg == "" or msg == None:
        message = str(item)+"\n"
    else:
        message = msg+" :: "+str(item)+"\n"
    try:
        if (os.path.isfile(log_path)):
            with open(log_path, "a") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+message)
        else:
            with open(log_path, "w") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+message)
    except FileExistsError as fileErr:
        print(fileErr.getMessage())
    except Exception as e:
        print(e.getMessage())


def get_stringFromItem(item: Any) -> str:
    result = ''
    if isinstance(item, KafkaLog):
        result = json.dumps(kafkaLog_toDict(item), ensure_ascii=False)
    elif isinstance(item, ClientLog):
        result = json.dumps(clientLog_toDict(item), ensure_ascii=False)
    elif isinstance(item, ClientLogDB):
        result = json.dumps(clientLogDB_toDict(item), ensure_ascii=False)
    elif isinstance(item, NboWithResponseLog):
        result = json.dumps(
            nboWithResponseLog_toDict(item), ensure_ascii=False)
    elif isinstance(item, NboLogDB):
        result = json.dumps(nboLogDB_toDict(item), ensure_ascii=False)
    elif isinstance(item, NboResponseLogDB):
        result = json.dumps(nboResponseLogDB_toDict(item), ensure_ascii=False)
    else:
        result = str(item)
    return result


def print_logFromKafkaServer(source, topic, key, value):
    sourceLogger.source_logger.info(
        "Created", extra={"topic": topic, "source": source, "key": key, "value": value})


def print_sourceText(item: Any, source: str, user: str, msg: str):
    dir_path = get_logFolderPath()
    log_path = os.path.join(dir_path, datetime.now().strftime(
        "%Y_%m_%d")+"_"+source+"_"+user+".txt")
    message = ""
    if msg == "" or msg == None:
        message = get_stringFromItem(item)+"\n"
    else:
        message = msg+" :: "+get_stringFromItem(item)+"\n"
    try:
        if (os.path.isfile(log_path)):
            with open(log_path, "a") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+source+" :: "+user+" :: " + message)
        else:
            with open(log_path, "w") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+source+" :: "+user+" :: " + message)
    except FileExistsError as fileErr:
        print(fileErr.getMessage())
    except Exception as e:
        print(e.getMessage())


def print_sourceInfo(message: str, item: Any, user: str, mode: str):
    if mode == '-p':
        type_name = type(item).__name__
        value = get_stringFromItem(item)
        extra = {"source": type_name, "user": user, "key": "", "value": value}
        sourceLogger.source_logger.info(message, extra=extra)
    elif mode == '-d':
        print_sourceText(item, type(item).__name__, user, message)
    else:
        raise ValueError("Wrong mode")


def print_httpText(msg: str, response: Response, item: Any, user: str):
    dir_path = get_logFolderPath()
    log_path = os.path.join(dir_path, datetime.now().strftime(
        "%Y_%m_%d")+"_http_"+user+".txt")
    message = ""
    if msg == "" or msg == None:
        message = str(item)+"\n"
    else:
        message = msg+" :: "+str(item)+"\n"
    http_str = str(response.status_code)+" :: "+str(response.reason)+" :: "+str(response.request.method)+" :: "+str(
        response.request.url)+" :: "+str(response.request.headers)+" :: "+response.text
    try:
        if (os.path.isfile(log_path)):
            with open(log_path, "a") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+http_str+" :: "+message)
        else:
            with open(log_path, "w") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+http_str+" :: "+message)
    except FileExistsError as fileErr:
        print(fileErr.getMessage())
    except Exception as e:
        print(e.getMessage())


def print_httpInfo(message: str, response: Response, item: Any, user: str, mode: str):
    if mode == '-p':
        value = "{}"
        if item is not None:
            value = get_stringFromItem(item)
        this_user = ""
        if user is not None or user != "":
            this_user = user
        httpLogger.http_logger.info(message, extra={
            "http_status": response.status_code,
            "http_reason": response.reason,
            "http_method": response.request.method,
            "http_uri": response.request.url,
            "http_headers": response.request.headers,
            "http_response": response.json(),
            "user": this_user,
            "value": value
        })
    elif mode == '-d':
        print_httpText(message, response, item, user)
    else:
        raise ValueError("Wrong mode")


def print_text(objectName: str, message: str, value: str):
    dir_path = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    log_path = os.path.join(dir_path, objectName+".txt")
    try:
        if (os.path.isfile(log_path)):
            with open(log_path, "a") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+message+"\n")
                if value != None or value != "":
                    file.write(value+"\n")
        else:
            with open(log_path, "w") as file:
                file.write(datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S")+" :: "+message+"\n")
                if value != None or value != "":
                    file.write(value+"\n")
    except FileExistsError as fileErr:
        print(fileErr.getMessage())
    except Exception as e:
        print(e.getMessage())

class ConsoleStats:
    def __init__(self)->None:
        self.consumerCounter = 0
        self.clientLogCounter = 0
        self.nboLogCounter = 0
        self.nboResponseLogCounter = 0
        self.noneLogCounter=0
        self.errorCounter = 0
        self.othersCounter = 0
        self.usersCounter = 0
        
    
    def raiseConsumerCounter(self):
        self.consumerCounter+=1
    def raiseClientLogCounter(self):
        self.clientLogCounter+=1
    def raiseNboLogCounter(self):
        self.nboLogCounter+=1
    def raiseNboResponseLogCounter(self):
        self.nboResponseLogCounter+=1
    def raiseNoneLogCounter(self):
        self.noneLogCounter+=1
    def raiseErrorCounter(self):
        self.errorCounter+=1
    def raiseOthersCounter(self):
        self.othersCounter+=1
    def setUsersCounter(self, users:int):
        self.usersCounter=users

    def getConsumerCounter(self):
        return str(self.consumerCounter)
    def getClientLogCounter(self):
        return str(self.clientLogCounter)
    def getNboLogCounter(self):
        return str(self.nboLogCounter)
    def getNboResponseLogCounter(self):
        return str(self.nboResponseLogCounter)
    def getNoneLogCounter(self):
        return str(self.noneLogCounter)
    def getErrorCounter(self):
        return str(self.errorCounter)
    def getOthersCounter(self):
        return str(self.othersCounter)
    def getUsersCounter(self, users:int):
        return str(self.usersCounter)

    def getStats(self):
        print("KL #"+self.getConsumerCounter+", where RA: "+self.getClientLogCounter + " | "+self.getNboLogCounter + 
              " | "+self.getNboResponseLogCounter +", N/A: " + self.getNoneLogCounter +
              ", EL: "+self.getErrorCounter +", OL: "+self.getOthersCounter +", Users: "+self.getUsersCounter)
         
        