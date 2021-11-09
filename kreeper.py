#!/usr/bin/env python3

# kreeper -- main
#   v1.0.6
#   by Luna Cordero
#   written 6/20/2021
#   updated 11/8/2021

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

# local imports
from source.client import connect
from source.market import analyze, compile, monitor
from source.orders import place_limit_order

# version -- update often!
VERSION = "1.0.6"

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
    parser.add_argument('--version', dest='version', action='store_true',
                        help='displays the current kreeper version')


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
if __name__ == "__main__":
    # parse arguments
    args = _parse_args()

    # connect client to API
    client = connect()

    run = True
    while run:
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
        markets = compile(
            client['market'],
            # args.coins or [key for key in balances.keys() if key != 'USD'], # default to all available coins
            args.coins or ['BTC', 'ETH', 'ADA', 'DOGE', 'SHIB'],
            args.quotes or ['USDT', 'USDC', 'BTC', 'ETH'],
            args.interval or '1hour', # default to one hour
            args.bars or 24, # default to number of hours in one day
        )

        print("done.\n")

        best = ('', 'buy', '0.00', '0.00')
        worst = ('', 'sell', str(float(math.inf)), str(float(math.inf)))

        # for each table
        for pair in markets.keys():
            # print out markets to terminal if --lines or --verbose are turned on
            if args.lines or args.verbose:
                monitor(pair, markets[pair], args.lines or 10, args.verbose or False) # default to 10 lines of data
            
            # analyze each table to determine action
            data = analyze(client['trade'], pair, markets[pair], balances)
            
            # check if it's the best buy out of all the positions being analyzed
            if ('buy' in data[1]):
                if (float(data[2]) > float(best[2])):
                    best = data
            elif ('sell' in data[1]):
                if (float(data[2]) < float(worst[2])):
                    worst = data
        
        if best[0] != '':
            place_limit_order(client['trade'], *best)
        if worst[0] != '':
            place_limit_order(client['trade'], *worst)
        
        print("done.\n")

        # run every few seconds. (should we change this or make it adjustable or smth?)
        time.sleep(1)
