import urllib.request
import json

DEFAULT_BASE = "USD"
DEFAULT_DATE = "latest"
API_URL_FORMAT = "http://api.fixer.io/{}?base={}&symbols={}"
API_URL_FORMAT_ALL = "http://api.fixer.io/{}?base={}"
BIG_NUM_MULTIPLY = 10**6
PRECISION = 4


class InvalidBaseException(Exception):
    pass


class InvalidDateException(Exception):
    pass


class CurrencyNotFoundException(Exception):
    pass


class CurrencyRate:
    def __init__(self, currency, base, date, rate):
        self.currency = currency
        self.base = base
        self.date = date
        self.rate = rate

    def __str__(self):
        return json.dumps(self.__dict__)


def get_rate(currency, base=DEFAULT_BASE, date=DEFAULT_DATE):
    url = API_URL_FORMAT.format(date, base, currency)
    try:
        body = urllib.request.urlopen(url).read()
        json_body = json.loads(body)
        if not json_body['rates']:
            raise CurrencyNotFoundException
        rate = list(json_body['rates'].items())[0]
        currency_rate = CurrencyRate(rate[0],
                                     json_body['base'],
                                     json_body['date'],
                                     round(rate[1], PRECISION))
        return currency_rate
    except urllib.error.URLError as e:
        body = e.read()
        json_body = json.loads(body)
        error_msg = json_body['error']
        if error_msg == 'Invalid base':
            raise InvalidBaseException
        else:
            raise InvalidDateException


def calculate_exchange(currency,
                       base_amount,
                       base=DEFAULT_BASE,
                       date=DEFAULT_DATE):
    if isinstance(currency, str):
        currency_rate = get_rate(currency, base, date)
        int_rate = int(currency_rate.rate * BIG_NUM_MULTIPLY)
        int_amount = int(base_amount * BIG_NUM_MULTIPLY)
        return round((int_rate * int_amount) / (BIG_NUM_MULTIPLY**2),
                     PRECISION)
    else:
        amount = base_amount
        for x in currency:
            amount = calculate_exchange(x, amount, base, date)
            base = x
        return amount


def currency_list():
    url = API_URL_FORMAT_ALL.format(DEFAULT_DATE, DEFAULT_BASE)
    body = urllib.request.urlopen(url).read()
    json_body = json.loads(body)
    l = list(json_body['rates'].keys())
    l.append(DEFAULT_BASE)
    return l


def check_exchange(
                    currency,
                    base_amount,
                    amount,
                    base=DEFAULT_BASE,
                    date=DEFAULT_DATE,
                    trust=0.2):
    calc_amount = calculate_exchange(currency, base_amount, base, date)
    if abs(calc_amount-amount)/calc_amount > trust:
        return False
    else:
        return True
