#!/usr/bin/env python3

# kreeper -- orders
#   v1.0.8
#   by Luna Cordero
#   written 11/4/2021
#   updated 11/28/2021

# function: place_limit_order
# input: client, pair, quantity, price
# output : none
# description: places a purchase or sale limit order
from flask.json import JSONDecoder, jsonify


def place_limit_order(client, order_dict):
    # place a limit order
    try:
        pair, action, quantity, price = order_dict["pair"], order_dict["action"], order_dict["quantity"], order_dict["price"]
        print('>>>\t' + action + 'ing', quantity, pair, "at", price, "\t<<<")
        order = client.create_limit_order(pair, action, quantity, price)
        print("order successful:", order)
        return { order.get_data() }
    except Exception as e:
        print("failed to make transaction: ", str(e))
        return str(e)
