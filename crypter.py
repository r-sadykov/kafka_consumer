#!/usr/bin/env python3

import argparse
from consumer.connector_crypter import Crypter

if __name__ == '__main__':
    # Parse the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config', dest='config_file',
                        type=str, required=True)
    parser.add_argument('-k', '--keys', dest='generateKeys', action='store_true')
    args = parser.parse_args()
    crypter = Crypter()
    if args.generateKeys:
        crypter.generate_keys()
    file_name = args.config_file
    crypter.encrypt_config(file_name)