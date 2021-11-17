#!/usr/bin/env python3

# kreeper -- main
#   by Luna Cordero
#   written 6/20/2021
#   updated 11/17/2021

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


import os
import ssl

from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


def start_server ():
    server_address = ('localhost', 8443)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
        server_side = True,
        certfile = 'ssl/62ba54b69c53d5bf.pem',
        keyfile = 'ssl/privkey.pem',
        # passphrase = os.getenv('SSL_PASSPHRASE'),
        ssl_version = ssl.PROTOCOL_TLS)
    
    httpd.serve_forever()

