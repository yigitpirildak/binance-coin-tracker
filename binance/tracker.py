import json
import time
import calendar
from threading import Thread
from binance.definitions import OrderSide, OrderStatus
from decimal import Decimal

class Tracker(Thread):

    def __init__(self, connection, interval=30):
        super().__init__()
        self.connection = connection
        self.tracking_list = []
        self.update_interval = interval

    def add_symbol(self, symbol):
        self.tracking_list.append(symbol)  # TODO : Check if symbol is correct?

    def run(self):
        while True:
            unrealized_total_profit_or_loss = 0
            for symbol in self.tracking_list:
                symbol_data = self.connection.all_orders(symbol, str(calendar.timegm(time.gmtime()) * 1000))  # TODO : Add a utility function to provide the timestamp in this format
                symbol_data_json = json.loads(symbol_data)
                average_cost_of_asset = 0
                total_balance = 0
                for order in symbol_data_json:
                    if order["status"] == OrderStatus.FILLED.value or order["status"] == OrderStatus.PARTIALLY_FILLED.value:
                        if order["side"] == OrderSide.BUY.value:
                            executed_qty = Decimal(order["executedQty"])
                            buy_cost = Decimal(order["cummulativeQuoteQty"])
                            price = buy_cost / executed_qty
                            average_cost_of_asset = ((average_cost_of_asset * total_balance) + (executed_qty * price)) / (total_balance + executed_qty)
                            total_balance += executed_qty
                        elif order["side"] == OrderSide.SELL.value:
                            executed_qty = Decimal(order["executedQty"])
                            total_balance -= executed_qty

                current_average_price = Decimal(json.loads(self.connection.current_average_price(symbol))["price"])  # TODO: This is not accurate (5min avg), use live data instead
                current_profit_or_loss = (current_average_price * total_balance) - (total_balance * average_cost_of_asset)
                print("======================================")
                print("Symbol = {}".format(symbol))
                print("Total balance = {}".format(total_balance))
                print("Average cost of asset = {}".format(average_cost_of_asset))
                print("Current profit/loss = {}".format(current_profit_or_loss))
                print("======================================")
                unrealized_total_profit_or_loss += current_profit_or_loss
            print("Unrealized Total Profit/Loss = {}".format(unrealized_total_profit_or_loss))
            time.sleep(self.update_interval)
