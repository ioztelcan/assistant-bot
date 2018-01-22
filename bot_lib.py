import sys
sys.path.insert(0, '/home/ioztelcan/projects/bitstamp-poc')
import bitstamp_poc

def get_bitcoin_price():
    price = bitstamp_poc.get_real_price()
    return "Current BTC price at Bitstamp is `{} EUR`".format(price)