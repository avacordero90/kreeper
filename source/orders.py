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
def place_limit_order(client, pair, action, quantity, price):        
    # place a limit order
    try:
        print('>>>\t' + action + 'ing', quantity, pair, "\t<<<")
        order = client.create_limit_order(pair, action, quantity, price)
        print("order successful:", order)
    except Exception as e:
        print("failed to make transaction: ", str(e))
    finally:
        return order
