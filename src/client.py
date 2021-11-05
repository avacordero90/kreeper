#!/usr/bin/env python3

# kreeper -- client
#   v1.0.4
#   by Luna Cordero
#   written 6/26/2021
#   updated 11/4/2021


import os
import sys

from kucoin.client import User, Trade, Market


# function: _connect_api
# input: none
# output: API client object
# description: connects the client to the API
def connect():
    # init

    print(os.environ.get('KUCOIN_KEY'))

    # check for environmental variables
    if (os.environ.get('KUCOIN_KEY') is None or os.environ.get('KUCOIN_SECRET') is None or os.environ.get('KUCOIN_PASSPHRASE') is None):
        sys.exit("ENVIRONMENTAL VARIABLES MISSING! declare KUCOIN_KEY, KUCOIN_SECRET, AND KUCOIN_PASSPHRASE to continue. run install.sh or config.sh if you know what you're doing, or see README.md for details.")

    # kucoin-python
    api_key = os.environ.get('KUCOIN_KEY')
    api_secret = os.environ.get('KUCOIN_SECRET')
    api_passphrase = os.environ.get('KUCOIN_PASSPHRASE')

    # build a set of API connections
    client = {}

    # User, Market, and Trade
    client['user'] = User(api_key, api_secret, api_passphrase)
    client['market'] = Market(url='https://api.kucoin.com')
    client['trade'] = Trade(api_key, api_secret, api_passphrase, is_sandbox=False, url='')

    return client