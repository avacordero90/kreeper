#!/usr/bin/env python3

# kreeper -- main
#   v1.0.7
#   by Luna Cordero
#   written 6/20/2021
#   updated 11/28/2021

# sources:
#   https://github.com/binance-us/binance-official-api-docs
#   https://github.com/sammchardy/python-binance
#   https://python-binance.readthedocs.io/en/latest/
#   https://github.com/sammchardy/python-kucoin
#   https://github.com/twopirllc/pandas-ta
#   https://www.roelpeters.be/many-ways-to-calculate-the-rsi-in-python-pandas/
#   https://docs.kucoin.com/
#   https://algotrading101.com/learn/binance-python-api-guide/
#   https://github.com/sammchardy/python-binance
#   https://www.investopedia.com/terms/r/rsi.asp
#   https://www.investopedia.com/terms/m/macd.asp
#   https://www.valutrades.com/en/blog/how-to-use-macd-and-rsi-together-to-spot-buying-opportunities
#   https://alternative.me/crypto/fear-and-greed-index/
#   https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory?select=coin_Ethereum.csv
#   https://github.com/twopirllc/pandas-ta#quick-start
#   https://github.com/Kucoin/kucoin-python-sdk

import argparse
import math
import os
import sys
import time
# from http.server import BaseHTTPRequestHandler, HTTPServer

from flask import Flask, jsonify, request
# from OpenSSL import SSL
import ssl

# local imports
from source.client import _connect
from source.markets import analyze, compile, monitor
from source.orders import place_limit_order
from source.server import start_server

# import requests


# version -- update often!
VERSION = "1.0.8"


app = Flask(__name__)


# function: _parse_args
# input: none
# output : args dict
# description: parses command line arguments for use by the program.
def _parse_args():
    # parse arguments
    parser = argparse.ArgumentParser(description='a kucoin service that buys and sells crypto based on technical analysis indicators')
    # parser.add_argument('-B', '--budget', dest='budget', type=int,
    #                     help='budget to trade with')
    parser.add_argument('-c', '--coins', dest='coins', type=str, nargs='+',
                        help='which coins to trade')
    parser.add_argument('-q', '--quotes', dest='quotes', type=str, nargs='+',
                        help='which quotes to trade against')
    parser.add_argument('-l', '--lines', dest='lines', type=int,
                        help='how many lines (datapoints) to display')
    parser.add_argument('-i', '--interval', dest='interval', type=str,
                        help='what interval of datapoints to display -- 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week')
    parser.add_argument('-b', '--bars', dest='bars', type=int,
                        help='how many bars to collect data from')
    parser.add_argument('-L', '--limit', dest='limit', type=int,
                        help='limit of datapoints to return')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='displays all logging and market data')
    parser.add_argument('-V', '--version', dest='version', action='store_true',
                        help='displays the current kreeper version')
    parser.add_argument('-k', '--key', dest='key', type=str,
                        help='API key')
    parser.add_argument('-s', '--secret', dest='secret', type=str,
                        help='API secret')
    parser.add_argument('-p', '--passphrase', dest='passphrase', type=str,
                        help='API passphrase')


    args = parser.parse_args()
    # print(args.coins)

    if args.version:
        sys.exit(VERSION)

    # if args.coins == None:
    #     sys.exit("no coins specified. please see " + os.path.basename(__file__) + " --help for more details.")

    if args.interval and args.interval not in ('1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '8hour', '12hour', '1day', '1week'):
        sys.exit("'" + args.interval + "' is not a valid interval! see " + os.path.basename(__file__) + " --help for more details.")

    if args.coins:
        args.coins = [string.upper() for string in args.coins]

    # if not args.budget:
    #     sys.exit("what's your budget? see " + os.path.basename(__file__) + " --help for more details.")

    return args


# main function
# program entry point
@app.route("/run_kreeper", methods = ['POST'])
def run_kreeper ():
    if request.method == 'POST':
        print(str(request))
        # return jsonify({"testing": "testing"})

        # parse arguments
        # args = _parse_args()
        kucoin_key = request.headers["kucoin-key"]
        kucoin_secret = request.headers["kucoin-secret"]
        kucoin_passphrase = request.headers["kucoin-passphrase"]

        args = request.get_json()
        # print(args)

        if "coins" in args and type(args["coins"]) is str:
            coins = [args["coins"]]
        elif "coins" in args and type(args["coins"]) is list:
            coins = args["coins"]
        else:
            coins = None
        
        # print(coins)

        if "quotes" in args and type(args["quotes"]) is str:
            quotes = [args["quotes"]]
        elif "quotes" in args and type(args["quotes"]) is list:
            quotes = args["quotes"]
        else:
            quotes = None

        if "interval" in args:
            interval = args["interval"]
        else:
            interval = None

        if "bars" in args:
            bars = args["bars"]
        else:
            bars = None

        if "lines" in args:
            lines = args["lines"]
        else:
            lines = None

        if "verbose" in args:
            verbose = args["verbose"]
        else:
            verbose = None

        # print(str(args))

        # connect client to API
        client = _connect(kucoin_key, kucoin_secret, kucoin_passphrase)

        # run = True
        # while run:
            
        # get balances for all assets & some account information
        print("getting balances ...")

        balances = {}

        # get account balances
        for account in client['user'].get_account_list():
            if account['type'] == 'trade':
                # balances = client['user'].get_account(account['id'])
                balances[account['currency']] = float(account['available'])
                if balances[account['currency']] > 0:
                    print (account['currency'], f"{balances[account['currency']]:8f}")

        print("done.\n")

        print("watching the markets ...")

        # build tables using pandas and technical analysis
        payload = {
            'client': client['market']
        }

        if coins:
            payload["coins"] = coins
        else:
            payload["coins"] = ['BTC', 'ETH', 'ADA', 'DOGE', 'SHIB']

        if quotes:
            payload["quotes"] = quotes
        else:
            payload["quotes"] = ['USDT', 'USDC', 'BTC', 'ETH']

        if interval:
            payload["interval"] = interval
        else:
            payload["interval"] = "1hour" # default to one hour

        if bars:
            payload["bars"] = bars
        else:
            payload["bars"] = 24 # default to number of hours in one day

        markets = compile(payload)

        print("done.\n")

        best = {"pair": '', "action": 'buy', "quantity": '0.00', "price": '0.00'}
        worst = {"pair": '', "action": 'sell', "quantity": str(float(math.inf)), "price": str(float(math.inf))}

        # for each table
        for pair in markets.keys():
            # print out markets to terminal if --lines or --verbose are turned on
            if lines or verbose:
                payload = {'pair': pair, 'pair_df': markets[pair], 'lines': args.lines or 10, 'verbose': args.verbose or False}
                monitor(payload) # default to 10 lines of data
            
            # analyze each table to determine action
            # url = 'https://api.kreeper.trade/kreeper'
            payload = {'pair': pair, 'table': markets[pair], 'balances': balances}
            # data = requests.get(url, data = payload)

            data = analyze(payload)
            
            # check if it's the best buy out of all the positions being analyzed
            if ('buy' in data["action"]):
                if (float(data["quantity"]) * float(data["price"]) > float(best["quantity"]) * float(data["price"])):
                    best = data
            elif ('sell' in data["action"]):
                if (float(data["quantity"]) * float(data["price"]) < float(worst["quantity"]) * float(data["price"])):
                    worst = data
        
        if best["pair"] != '':
            return jsonify(place_limit_order(client['trade'], best))
        if worst["pair"] != '':
            return jsonify(place_limit_order(client['trade'], worst))
        
        # run every few seconds. (should we change this or make it adjustable or smth?)
        # time.sleep(1)


@app.route('/')
def index():
    return 'Flask is running!'


if __name__ == '__main__':  
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('ssl/62ba54b69c53d5bf.pem', keyfile='ssl/privkey.pem')
    # context.use_privatekey_file('ssl/privkey.pem')
    # context.use_certificate_file('ssl/62ba54b69c53d5bf.pem')
    # context = ('ssl/62ba54b69c53d5bf.pem', 'ssl/privkey.pem')
    app.run(host='0.0.0.0', port=443, debug=True, threaded=True, ssl_context=context)

# # main function
# # program entry point
# if __name__ == "__main__":
#     kreeper_data = run_kreeper()

#     for kd in kreeper_data:
#         # time.sleep(1)
#         print(kd)
