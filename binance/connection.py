from binance.commands import *

class BinanceConnection:

    API_LIST = ["https://api1.binance.com/", "https://api2.binance.com/", "https://api3.binance.com/"]

    def __init__(self, api_key, secret_key=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_index = 0

    def set_api_index(self, api_index):
        if api_index >= 0 and api_index < len(self.API_LIST):
            self.api_index = api_index
        else:
            raise Exception("API index is out of range, API_LIST = " + str(self.API_LIST))

    def get_all(self, timestamp, recv_window=None):
        return BinanceGetAll(self.API_LIST[self.api_index], self.api_key, self.secret_key, timestamp, recv_window).send()

    def get_future_account_transaction_history(self, asset, start_time, timestamp, end_time=None, current=None, size=None, recv_window=None):
        return BinanceGetFutureAccountTransactionHistory(self.API_LIST[self.api_index], self.api_key, self.secret_key, asset, start_time, timestamp, end_time, current, size, recv_window).send()

    def recent_trades_list(self, symbol, limit=None):
        return BinanceRecentTradesList(self.API_LIST[self.api_index], self.api_key, symbol, limit).send()

    def current_average_price(self, symbol):
        return BinanceCurrentAveragePrice(self.API_LIST[self.api_index], self.api_key, symbol).send()

    def all_orders(self, symbol, timestamp, orderId=None, startTime=None, endTime=None, limit=None, recvWindow=None):
        return BinanceAllOrders(self.API_LIST[self.api_index], self.api_key, self.secret_key, symbol, timestamp, orderId, startTime, endTime, limit, recvWindow).send()
