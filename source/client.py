#!/usr/bin/env python3

# kreeper -- client
#   v1.0.8
#   by Luna Cordero
#   written 6/26/2021
#   updated 11/28/2021


import os
import sys

from kucoin.client import User, Trade, Market


# function: _connect_api
# input: none
# output: API client object
# description: connects the client to the API
def _connect(api_key=None, api_secret=None, api_passphrase=None):
    # init

    print(os.environ.get('KUCOIN_KEY'))

    if (api_key is None or api_secret is None or api_passphrase is None):
        # check for environmental variables
        if (os.environ.get('KUCOIN_KEY') is None or os.environ.get('KUCOIN_SECRET') is None or os.environ.get('KUCOIN_PASSPHRASE') is None):
            sys.exit("ENVIRONMENTAL VARIABLES MISSING! declare KUCOIN_KEY, KUCOIN_SECRET, AND KUCOIN_PASSPHRASE to continue. run install.sh or config.sh if you know what you're doing, or see README.md for details.")

    # kucoin-python
    api_key = api_key or os.environ.get('KUCOIN_KEY')
    api_secret = api_secret or os.environ.get('KUCOIN_SECRET')
    api_passphrase = api_passphrase or os.environ.get('KUCOIN_PASSPHRASE')

    # build a set of API connections
    client = {}

    # User, Market, and Trade
    client['user'] = User(api_key, api_secret, api_passphrase)
    client['market'] = Market(url='https://api.kucoin.com')
    client['trade'] = Trade(api_key, api_secret, api_passphrase, is_sandbox=False, url='')

    return client