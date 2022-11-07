import os
from alpha_vantage.foreignexchange import ForeignExchange


def get_current_exchange_rate(from_currency, to_currency):
    try:
        fe = ForeignExchange(key=str(os.getenv('ALPHAVANTAGE_API_KEY')))
        data, _ = fe.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
        exchange_rate = round(float(data['5. Exchange Rate']), 2)
        return exchange_rate
    except Exception:
        return "Error"
