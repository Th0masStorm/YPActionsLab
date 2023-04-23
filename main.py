#!/usr/bin/env python3
import json
from flask import Flask, request
from pycoingecko import CoinGeckoAPI

app = Flask(__name__)
COINGECKO_API_CLIENT = CoinGeckoAPI()

SUPPORTED_TICKERS: dict[str, str] = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'ltc': 'litecoin',
}

SUPPORTED_FIATS: set[str] = {'usd', 'eur'}

class CoinNotFoundException(Exception):
    pass

class FiatNotFoundException(Exception):
    pass


def ticker_to_coingecko_id(ticker: str) -> str:
    try:
        return SUPPORTED_TICKERS[ticker]
    except KeyError:
        raise CoinNotFoundException(f'Ticker {ticker} is not supported')


def get_rate_from_coingecko(base_currency: str, quote_currency: str) -> float:
    response = COINGECKO_API_CLIENT.get_price(ids=base_currency, vs_currencies=quote_currency)
    if len(response) == 0:
        return None
    try:
        return float(response[base_currency][quote_currency])
    except KeyError:
        raise FiatNotFoundException(quote_currency)

@app.route("/")
def handle_index() -> str:
    return json.dumps({"msg": "hello, practicum students!"})

@app.route("/rate")
def handle_rate() -> str:
    args = request.args.to_dict()
    base_ticker = args.get('base')
    if base_ticker is None:
        return json.dumps({'rate': '', 'msg': 'Base not provided'})
    quote_currency = args['quote']
    if quote_currency is None:
        return json.dumps({'rate': '', 'msg': 'Quote not provided'})
    try:
        base_currency = ticker_to_coingecko_id(base_ticker.lower())
        rate = get_rate_from_coingecko(base_currency, quote_currency)
    except CoinNotFoundException:
        return json.dumps({'rate': '', 'msg': 'Base not supported'})
    except FiatNotFoundException:
        return json.dumps({'rate': '', 'msg': 'Fiat not supported'})

    return json.dumps({'rate': rate, 'msg': 'OK'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')