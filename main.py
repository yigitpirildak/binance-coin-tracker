from binance.connection import BinanceConnection
import time
import calendar

# Starter code
if __name__ == "__main__":
    binance_connection = BinanceConnection("API_KEY", "API_SECRET")
    timestamp_in_ms = str(calendar.timegm(time.gmtime()) * 1000)
    get_all_response = binance_connection.get_all(timestamp_in_ms)
    print(get_all_response)
