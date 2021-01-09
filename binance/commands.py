import requests
import hmac
import hashlib
from abc import ABC
from enum import Enum


class CallInfo(Enum):
    GET_ALL = ["GET", "/sapi/v1/capital/config/getall"]

class BinanceApiCall(ABC):

    def __init__(self, api, api_key, call_info, params):
        self.api = api
        self.api_key = api_key
        self.request = requests.Request(call_info.value[0],
                                        self.api + call_info.value[1],
                                        params=params,
                                        headers={'X-MBX-APIKEY': api_key})

    def send(self):
        self.send_prepared_request(self.request.prepare())

    def send_prepared_request(self, prepared_request):
        with requests.Session() as session:
            return session.send(prepared_request).content

class BinanceUserDataApiCall(BinanceApiCall, ABC):

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
        print(prepared_request.url)
        return self.send_prepared_request(prepared_request)

class BinanceGetAll(BinanceUserDataApiCall):

    def __init__(self, api, api_key, secret_key, timestamp, recvWindow=None):
        self.__init_params(timestamp, recvWindow)
        super().__init__(api, api_key, CallInfo.GET_ALL, self.params, secret_key)

    def __init_params(self, timestamp, recvWindow):
        self.params = {}
        self.params["timestamp"] = timestamp
        self.params["recvWindow"] = recvWindow
