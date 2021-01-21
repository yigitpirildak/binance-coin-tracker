import json
import time
import calendar
from threading import Thread
from binance.definitions import OrderSide

class Tracker(Thread):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.tracking_list = []

    def add_symbol(self, symbol):
        self.tracking_list.append(symbol)  # TODO : Check if symbol is correct

    def run(self):
        for symbol in self.tracking_list:
            symbol_data = self.connection.all_orders(symbol, str(calendar.timegm(time.gmtime()) * 1000))
            symbol_data_json = json.loads(symbol_data)
            bought = 0
            sold = 0
            for order in symbol_data_json:
                if order["status"] == "FILLED":
                    if order["side"] == OrderSide.BUY.value:
                        bought += float(order["executedQty"])
                    elif order["side"] == OrderSide.SELL.value:
                        sold += float(order["executedQty"])

            print("Total balance = {}".format(bought - sold))
