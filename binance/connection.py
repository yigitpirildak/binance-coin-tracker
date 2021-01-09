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

    def get_all(self, timestamp, recvWindow=None):
        return BinanceGetAll(self.API_LIST[self.api_index], self.api_key, self.secret_key, timestamp, recvWindow).send()
