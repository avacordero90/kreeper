#!/usr/bin/env python3

# kreeper -- market
#   v1.0.6
#   by Luna Cordero
#   written 6/26/2021
#   updated 11/8/2021


import pandas
import pandas_ta
import sys
import time

from datetime import datetime

# local imports
from source.orders import place_limit_order

from kreeper.mysteries import analyze

# function: compile
# input: client object, coins str list, quotes str list, interval str, bars int
# output: coin dataframe list
# description: creates and cleans up a list of dataframes containing a market data about a coin
# def compile(coins, lines, interval, bars, limit):
def compile(client, coins, quotes, interval, bars):
    # build a list of tables (dataframes)
    tables = {}

    # build a list of all symbols on exchange
    symbols = [symbol['symbol'] for symbol in client.get_symbol_list()]

    for coin in coins:
        for quote in quotes:
            if (coin + "-" + quote) in symbols:
                print("getting market data for " + coin + "-" + quote + " ...")
                time.sleep(1) # for rate limiting purposes

                try:
                    bars = client.get_kline(coin + "-" + quote, interval)

                    # print(bars)
                    
                    if bars:
                        # it seems like kucoin returns the datapoints in reverse order so...
                        bars.reverse()

                        # clean data - just keep datetime, open, high, low, close, amount, volume
                        for line in bars:
                            line[0] = datetime.fromtimestamp(int(line[0]))
                            line[1] = float(line[1])
                            line[2] = float(line[2])
                            line[3] = float(line[3])
                            line[4] = float(line[4])
                            line[5] = float(line[5])
                            line[6] = float(line[6])
                            
                        # create a Pandas DataFrame

                        #python-kucoin
                        pair_df = pandas.DataFrame(bars, columns=['datetime', 'open', 'close', 'high', 'low', 'amount', 'volume'])

                        # Here is how we can calculate the RSI using the pandas-ta library
                        rsi = pandas_ta.rsi(pair_df['close'], length=14)

                        # Here is how we can calculate the MACD using the pandas-ta library -- i think?
                        macd = pandas_ta.macd(pair_df['close'], length=bars)

                        # Finally, we will join our RSI and MACD values to our original DataFrame
                        # join the rsi and macd calculations as columns in original df
                        pair_df = pair_df.join([rsi, macd])

                        # set the datetime as the table index
                        pair_df.set_index('datetime', inplace=True)
                
                        tables[coin + "-" + quote] = pair_df

                except Exception as e:
                    print("failed to get market data for " + coin + "-" + quote + ": " + str(e))
            
    if not tables:
        sys.exit('no available coins in your market !!!')

    return tables

# function: monitor
# input: pair str, pair dataframe.
# output: none
# description: prints market data for a given pair
def monitor(pair, pair_df, lines=None, verbose=False):
    print(pair)
    if lines:
        print(pair_df.tail(lines))
    else:
        print(pair_df)

    if verbose:
        # find the current rsi
        current_rsi = pair_df['RSI_14'][-1]

        # find the histogram
        # TODO -- this needs to check for macd crossing signal going up!
        current_histogram = pair_df['MACDh_12_26_9'][-1]
        print(pair, 'rsi:', current_rsi)
        print(pair, 'histogram:', current_histogram)

    print()