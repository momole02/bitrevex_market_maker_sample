####################################################################
# market_maker.py
####################################################################
# Bitrevex market maker class definition
####################################################################
# Project : Bitrevex market maker
# For the Bitrevex Meet Up 1st session
####################################################################


from bitrevex_interface import *

class MarketMakerError(RuntimeError):
    def __init__(self, message, api_message=None):
        self.message=message
        self.api_message=api_message
        self.args="{}.{}".format(message, api_message)


'''
Bitrevex based market making strategy implementation
'''
class MarketMaker:


    '''
    Initializes a new market maker
    want_asset : left pair asset
    offer_asset : right pair asset
    spread_ratio: the spread ratio used, more it's low more the algorithm is agressive
    balance_ratio : the balance (for offer asset) used each orders (buy/sell)
    api_key : bitrevex API key
    '''
    def __init__(self, want_asset, offer_asset, spread_ratio, balance_ratio, api_key):
        self.pair='{}/{}'.format(want_asset, offer_asset)
        self.want_asset=want_asset
        self.offer_asset=offer_asset
        self.spread_ratio = spread_ratio
        self.balance_ratio = balance_ratio
        self.api_key=api_key


    '''
    Compute order data (spread & MID price)
    '''
    def compute_order_data(self):

        # get our open orders
        bi = BitrevexInterface('trade', self.api_key)

        open_sell_orders = bi.callRPCMethod('getAllOpenOrders', {
            'want_symbol':self.want_asset,
            'offer_symbol':self.offer_asset,
            'order_side':'ASK',
            'order_type':'LIMIT'
        })

        open_sell_orders = open_sell_orders + bi.callRPCMethod('getAllOpenOrders', {
            'want_symbol': self.want_asset,
            'offer_symbol': self.offer_asset,
            'order_side': 'ASK',
            'order_type': 'MARKET'
        })

        open_buy_orders = bi.callRPCMethod('getAllOpenOrders', {
            'want_symbol':self.want_asset,
            'offer_symbol':self.offer_asset,
            'order_side':'BID',
            'order_type':'LIMIT'
        })

        open_buy_orders = open_buy_orders + bi.callRPCMethod('getAllOpenOrders', {
            'want_symbol': self.want_asset,
            'offer_symbol': self.offer_asset,
            'order_side': 'BID',
            'order_type': 'MARKET'
        })

        try:
            sell_prices = [float(order['price']) for order in open_sell_orders]

            buy_prices = [float(order['price']) for order in open_buy_orders]

            if sell_prices == [] or buy_prices == []:
                raise MarketMakerError("Missing sell orders or buy orders in the market {}".format(self.pair))

            min_sell_price = min(sell_prices)

            max_buy_price = max(buy_prices)

            # compute the spread
            spread = min_sell_price - max_buy_price

            # compute the middle price
            mid_price = (min_sell_price + max_buy_price) / 2

            return {'spread': spread, 'mid_price': mid_price}

        except BitrevexError as err:
            raise MarketMakerError('Error on {}'.format(self.pair), err.message)

    '''
    Compute the quantity to buy/sell by the price
    '''
    def compute_quantity(self, price):
        try:
            bi=BitrevexInterface('funds', self.api_key)

            # the trade balance of the offer asset
            offer_balance = bi.callRPCMethod('getBalance' , {
                'type':"2",
                'symbol':self.offer_asset
            })

            # the trade balance of the want asset
            want_balance = bi.callRPCMethod('getBalance',{
                'type':'2',
                'symbol':self.want_asset
            })

            offer_balance_total, want_balance_total = float(offer_balance['balance']),float(want_balance['balance'])

            # compute the right quantity to buy/sell
            right_amount = self.balance_ratio*offer_balance_total/price

            # compute the max amount to buy/sell
            avail_amount = self.balance_ratio*want_balance_total

            # let's take the min
            return min(right_amount, avail_amount)

        except BitrevexError as err:
            raise MarketMakerError('Error on {}'.format(self.pair), err.message)

    '''
    Send an order based on parameters
    '''
    def sendOrder(self):

        try:

            order_data = self.compute_order_data()

            spread, mid_price = order_data['spread'], order_data['mid_price']

            # compute the buy order price
            buy_price = mid_price*(1-self.spread_ratio)

            # compute the sell order price
            sell_price = mid_price*(1+self.spread_ratio)

            # compute the good quantity
            quantity=self.compute_quantity(buy_price)

            bi = BitrevexInterface('trade', self.api_key)

            # send the buy order
            bi.callRPCMethod('sendOrder', {
                'want_symbol': self.want_asset,
                'offer_symbol': self.offer_asset,
                'side': 'BID',
                'type': 'LIMIT',
                'price': '{:.8f}'.format(buy_price), # format with 8 decimal numbers
                'amount': '{:.8f}'.format(quantity)
            })

            # send the sell order
            bi.callRPCMethod('sendOrder',{
                'want_symbol': self.want_asset,
                'offer_symbol': self.offer_asset,
                'side': 'ASK',
                'type': 'LIMIT',
                'price': '{:.8f}'.format(sell_price),
                'amount': '{:.8f}'.format(quantity)
            })

            return {
                'pair': self.pair,
                'quantity':quantity,
                'spread': spread,
                'mid_price': mid_price,
                'buy_price': buy_price,
                'sell_price': sell_price
            }

        except BitrevexError as err:
            raise MarketMakerError('Error on {}'.format(self.pair), err.message)