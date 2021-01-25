import time
import calendar
from binance.connection import BinanceConnection
from binance.tracker import Tracker

# Starter code
if __name__ == "__main__":
    binance_connection = BinanceConnection("API_KEY", "API_SECRET")
    coin_tracker = Tracker(binance_connection)
    coin_tracker.add_symbol("EOSUSDT")  # TODO : Add a mode to grab available coins from wallet
    coin_tracker.add_symbol("ADAUSDT")
    coin_tracker.add_symbol("SUSHIUSDT")
    coin_tracker.add_symbol("ETHUSDT")
    coin_tracker.add_symbol("BCHUSDT")
    coin_tracker.start()
