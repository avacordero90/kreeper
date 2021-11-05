#!/usr/bin/env python3

# kreeper -- market
#   v1.0.4
#   by Luna Cordero
#   written 6/26/2021
#   updated 11/4/2021


import pandas
import pandas_ta
import sys
import time

# from kucoin.exceptions import KucoinAPIException

from datetime import datetime

# local imports
from src.orders import place_limit_order

# function: analyze
# input: client object, pair name, pair table dataframe object, balances dict
# output: quantity to buy or sell
# description: analyzes dataframe to decide what to do with stock based on 
def analyze(client, pair, table, balances):
    # find the current rsi
    current_rsi = table['RSI_14'][-1]

    # find the histogram
    # ??? -- this needs to check for macd crossing the signal going up!
    current_histogram = table['MACDh_12_26_9'][-1]

    # ??? -- probability table
    # ??? -- decide what to do based on rsi and macd
    # ??? -- base specific actions here off of risk factor set by user
    #   example: $ python3 kreeper.py -R [1 or 2 or 3], --risk-factor [1 or 2 or 3]
    # ??? -- engage ML logic when unsure
    #   example: $ python3 kreeper.py -ML, --machine-learning

    coin = pair.split("-")[0]
    quote = pair.split("-")[1]
    action = ""
    quantity = 0
    price = 0

    if (current_rsi < 30 or current_histogram < 0) and coin in balances:
        coin_balance = balances[coin]
        if quote in balances:
            quote_balance = balances[quote]
        else:
            quote_balance = 0

        if coin_balance > 0:
            # sell pair

            # find the last closing price
            price = table['close'][-1]

            # the quote currency balance, plus the coin balance times the price (i.e. the potential value of the bid),
            # times the rsi percentage  is how much should be invested
            # example:
            #   (USDT 100.00 + (ETH 1.00 * USDT 4300.00) * (70 / 100))
            #   (USDT 100.00 + USDT 4300.00) * 0.70
            #   USDT 4400.00 * 70%
            #   USDT 3080 <-- investment--should be equal to the coin balance times the price. if it's not, make it so.
            investment = (quote_balance + (coin_balance * price)) * (1 - (current_rsi / 100))

            # print(investment, (coin_balance * price * 1.10))

            # if the investment amount is less than what's in there, with a 10% wiggle room...
            if (investment < coin_balance * price * 0.90):
                # determine the appropriate quantity to sell
                # quantity = investment - coin_balance

                # or just sell the entire coin balance?
                quantity = coin_balance
                action = "sell"

                print('>>>\tselling', quantity, pair, "\t<<<")

                time.sleep(1) # rate limit pause

                # place a limit sell order
                # place_limit_order(pair, 'sell', str(round(quantity, 4)), str(price))

    elif (current_rsi > 50 and current_histogram > 0) and quote in balances:
    # if rsi is over 50, histogram has crossed, and the current balance of the asset is lower than ...
        quote_balance = balances[quote] or 0
        if coin in balances:
            coin_balance = balances[coin]
        else:
            coin_balance = 0

        if quote_balance > 0:
            # buy pair

            # find the last closing price
            price = table['close'][-1]

            # the quote currency balance, plus the coin balance times the price (i.e. the potential value of the bid),
            # times the rsi percentage is how much should be invested
            # example:
            #   (USDT 100.00 + (ETH 1.00 * USDT 4300.00) * (70 / 100))
            #   (USDT 100.00 + USDT 4300.00) * 0.70
            #   USDT 4400.00 * 70%
            #   USDT 3080 <-- investment--should be equal to the coin balance times the price. if it's not, make it so.
            investment = (quote_balance + (coin_balance * price)) * (current_rsi / 100)

            # print(investment, (coin_balance * price * 1.10))

            # if the investment amount is more than what's in there, with a 10% wiggle room...
            if (investment > coin_balance * price * 1.10):
                # determine the appropriate quantity to buy
                quantity = (investment / price) - coin_balance
                action = "buy"

                # print('>>>\tbuying', quantity, pair, "\t<<<")

                time.sleep(1) # rate limit pause
                
                # place a limit buy order
                # try:
                #     order = client.create_limit_order(pair, 'buy', str(round(quantity, 4)), str(price))
                # except Exception as e:
                #     print("failed to make transaction: ", str(e))
    # else:
    #     print('hodling', pair, ' ...')
    print(pair, action, str(round(quantity, 5)), str(price))
    return (pair, action, str(round(quantity, 5)), str(price))

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