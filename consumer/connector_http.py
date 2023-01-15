import requests
from consumer.connector_crypter import Crypter
from consumer.connector_logger import print_errorInfo, print_httpInfo


def putToDb(url, source, user, obj):
    data = {"metadata": source, "userLogin": user, "json": obj}
    session = requests.Session()
    retries = 5
    while retries > 0:
        try:
            response = session.post(url, json=data)
            if response.status_code == requests.codes.ok:
                if response.json()["result"] == False:
                    print_httpInfo(
                        "Failed to put into DB via Reason case", response, obj, user, "-p")
                    return False
                return True
            print_httpInfo("Failed to put into DB", response, obj, user, "-p")
        except Exception as e:
            print_errorInfo(e)
            retries -= 1
            pass
    return False


def get_users(url):
    session = requests.Session()
    retries = 5
    while retries > 0:
        try:
            response = session.get(url)
            if response.status_code != requests.codes.ok or response.json()["result"] == False:
                print_httpInfo("Error", response, "", "", "-p")
            return response.json()["result"]
        except Exception as e:
            print_errorInfo(e)
            retries -= 1
    return None


def get_token(url, config_file):
    data = {"request": "token_1"}
    session = requests.Session()
    retries = 5
    while retries > 0:
        try:
            response = session.post(url, json=data)
            private_key = response.json()["result"]
            crypter = Crypter()
            token = crypter.decrypt_config(
                filename=config_file, private_key=private_key)
            return token
        except Exception as e:
            print_errorInfo(e)
            retries -= 1
    return None
