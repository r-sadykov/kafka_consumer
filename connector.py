#!/usr/bin/env python3

import argparse
import threading
import time
from consumer.connector_configer import KafkaConsumer
import consumer.connector_globals as globals
from consumer.connector_http import get_token, get_users


if __name__ == '__main__':
    # Parse the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config', dest='config_file',
                        type=str, required=True)
    parser.add_argument('-r', '--reset', dest='reset', action='store_true')
    parser.add_argument('-k', '--key', dest='url', type=str)
    args = parser.parse_args()

    globals.__init__()
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    data = ""
    if args.url is not None:
        data = get_token(args.url, args.config_file)
    else:
        with open(args.config_file, 'r') as f:
            data = f.read()
    globals.config_parser.read_string(data)
    if data == "" or data is None:
        print("No config data!")
        exit()

    cons = KafkaConsumer(globals.config_parser, isReset=args.reset)
    cons.subscribe()

    def consume(cons):
        semaphore.acquire()
        cons.consume()
        semaphore.release()

    def set_users():
        while True:
            semaphore.acquire()
            url = globals.config_parser['connections']['get_users_url']
            globals.users = get_users(url[1:-1])
            if globals.users is not None:
                globals.prev_users = globals.users
            time.sleep(60)
            semaphore.release()
            
    def console():
        semaphore.acquire()
        globals.stats.getStats()
        time.sleep(globals.config_parser['filters']['frequency'])
        semaphore.release()

    semaphore = threading.BoundedSemaphore(2)
    th1 = threading.Thread(target=consume, args=(cons,))
    th1.daemon = False
    th1.start()
    th2 = threading.Thread(target=set_users)
    th2.daemon = True
    th2.start()
    th3 = threading.Thread(target=console)
    th3.daemon = True
    th3.start()
