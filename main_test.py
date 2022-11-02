from types import NoneType
import main
import unittest

class TestMain(unittest.TestCase):

    get_rate_test_cases = [
        ('bitcoin', 'usd', None), # happy path
    ]
    def test_ticker_to_coingecko_id(self):
        self.assertEqual(main.ticker_to_coingecko_id('BTC'), 'bitcoin') # happy path
        with self.assertRaises(main.CoinNotFoundException):
            main.ticker_to_coingecko_id('NOEXIST')

    def test_get_rate_from_coingecko(self):
        self.assertIsInstance(main.get_rate_from_coingecko('bitcoin', 'usd'), float)
        self.assertIsInstance(main.get_rate_from_coingecko('noexist', 'usd'), NoneType)
        with self.assertRaises(main.FiatNotFoundException):
            main.get_rate_from_coingecko('bitcoin', 'noexist')

