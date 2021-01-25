import requests
import hmac
import hashlib
from abc import ABC
from enum import Enum


class CallInfo(Enum):
    # USER_DATA (SIGNED)
    GET_ALL = ["GET", "sapi/v1/capital/config/getall"]
    GET_FUTURE_ACCOUNT_TRANSACTION_HISTORY_LIST = ["GET", "sapi/v1/futures/loan/repay/history"]
    ALL_ORDERS = ["GET", "api/v3/allOrders"]

    # NONE
    RECENT_TRADES_LIST = ["GET", "api/v3/trades"]
    CURRENT_AVERAGE_PRICE = ["GET", "api/v3/avgPrice"]

class BinanceApiCall(ABC):

    def __init__(self, api, api_key, call_info, params):
        self.api = api
        self.api_key = api_key
        self.request = requests.Request(call_info.value[0],
                                        self.api + call_info.value[1],
                                        params=params,
                                        headers={'X-MBX-APIKEY': api_key})

    def send(self):
        return self.send_prepared_request(self.request.prepare())

    def send_prepared_request(self, prepared_request):
        print("Calling endpoint = {0}".format(prepared_request.url))
        with requests.Session() as session:
            return session.send(prepared_request).content

    def init_params(self, param_list, required, optional):
        all_params = required + optional
        parameter_map = {}
        if len(all_params) != len(param_list):
            raise Exception("Number of parameters do not match!")

        i = 0
        for required_parameter in required:
            if param_list[i] is None:
                raise Exception("{0} is a required parameter which cannot be None!".format(required[i]))
            parameter_map[required_parameter] = param_list[i]
            i = i + 1

        for optional_parameter in optional:
            parameter_map[optional_parameter] = param_list[i]
            i = i + 1

        return parameter_map

class BinanceSignedApiCall(BinanceApiCall, ABC):

    def __init__(self, api, api_key, call_info, params, secret_key):
        super().__init__(api, api_key, call_info, params)
        self.secret_key = secret_key

    def send(self):
        prepared_request = self.request.prepare()
        total_params = prepared_request.body if prepared_request.body is not None else ""
        if self.request.params is not None and len(self.request.params) != 0:
            query_string = prepared_request.url.replace(self.request.url + "?", "", 1)
            total_params = query_string + total_params
        signature = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(total_params, encoding='utf8'), digestmod=hashlib.sha256)
        prepared_request.prepare_url(prepared_request.url, {"signature": signature.hexdigest()})
        return self.send_prepared_request(prepared_request)

class BinanceGetAll(BinanceSignedApiCall):

    REQUIRED_PARAMS = ["timestamp"]
    OPTIONAL_PARAMS = ["recvWindow"]

    def __init__(self, api, api_key, secret_key, timestamp, recv_window=None):
        params = self.init_params([timestamp, recv_window], self.REQUIRED_PARAMS, self.OPTIONAL_PARAMS)
        super().__init__(api, api_key, CallInfo.GET_ALL, params, secret_key)

class BinanceGetFutureAccountTransactionHistoryList(BinanceSignedApiCall):

    REQUIRED_PARAMS = ["asset", "startTime", "timestamp"]
    OPTIONAL_PARAMS = ["endTime", "current", "size", "recvWindow"]

    def __init__(self, api, api_key, secret_key, asset, start_time, timestamp, end_time=None, current=None, size=None, recv_window=None):
        params = self.init_params([asset, start_time, timestamp, end_time, current, size, recv_window], self.REQUIRED_PARAMS, self.OPTIONAL_PARAMS)
        super().__init__(api, api_key, CallInfo.GET_FUTURE_ACCOUNT_TRANSACTION_HISTORY_LIST, params, secret_key)

class BinanceAllOrders(BinanceSignedApiCall):

    REQUIRED_PARAMS = ["symbol", "timestamp"]
    OPTIONAL_PARAMS = ["orderId", "startTime", "endTime", "limit", "recvWindow"]

    def __init__(self, api, api_key, secret_key, symbol, timestamp, orderId=None, startTime=None, endTime=None, limit=None, recvWindow=None):
        params = self.init_params([symbol, timestamp, orderId, startTime, endTime, limit, recvWindow], self.REQUIRED_PARAMS, self.OPTIONAL_PARAMS)
        super().__init__(api, api_key, CallInfo.ALL_ORDERS, params, secret_key)


class BinanceRecentTradesList(BinanceApiCall):

    REQUIRED_PARAMS = ["symbol"]
    OPTIONAL_PARAMS = ["limit"]

    def __init__(self, api, api_key, symbol, limit=None):
        params = self.init_params([symbol, limit], self.REQUIRED_PARAMS, self.OPTIONAL_PARAMS)
        super().__init__(api, api_key, CallInfo.RECENT_TRADES_LIST, params)

class BinanceCurrentAveragePrice(BinanceApiCall):

    REQUIRED_PARAMS = ["symbol"]
    OPTIONAL_PARAMS = []

    def __init__(self, api, api_key, symbol):
        params = self.init_params([symbol], self.REQUIRED_PARAMS, self.OPTIONAL_PARAMS)
        super().__init__(api, api_key, CallInfo.CURRENT_AVERAGE_PRICE, params)
