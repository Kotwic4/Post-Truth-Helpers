import urllib.request
import json

DEFAULT_BASE = "USD"
DEFAULT_DATE = "latest"
API_URL_FORMAT = "http://api.fixer.io/{}?base={}&symbols={}"
API_URL_FORMAT_ALL = "http://api.fixer.io/{}?base={}"
VALUE_PRECISION = 10**5


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


def generate_url(currency, base=DEFAULT_BASE, date=DEFAULT_DATE):
    return API_URL_FORMAT.format(date, base, currency)


def get_currency_rate(currency, base=DEFAULT_BASE, date=DEFAULT_DATE):
    url = generate_url(currency, base, date)
    try:
        body = urllib.request.urlopen(url).read()
        json_body = json.loads(body)
        if not json_body['rates']:
            raise CurrencyNotFoundException
        rate = list(json_body['rates'].items())[0]
        currency_rate = CurrencyRate(rate[0],
                                     json_body['base'],
                                     json_body['date'],
                                     rate[1])
        return currency_rate
    except urllib.error.URLError as e:
        body = e.read()
        json_body = json.loads(body)
        error_msg = json_body['error']
        if error_msg == 'Invalid base':
            raise InvalidBaseException
        else:
            raise InvalidDateException


def calculate_currency_exchange(currency,
                                amount,
                                base=DEFAULT_BASE,
                                date=DEFAULT_DATE):
    if isinstance(currency, str):
        currency_rate = get_currency_rate(currency, base, date)
        a = int(currency_rate.rate * VALUE_PRECISION)
        b = int(amount * VALUE_PRECISION)
        return ((a * b)//VALUE_PRECISION)/VALUE_PRECISION
    else:
        for x in currency:
            amount = calculate_currency_exchange(x, amount, base, date)
            base = x
        return amount


def get_currency_list():
    url = API_URL_FORMAT_ALL.format(DEFAULT_DATE, DEFAULT_BASE)
    body = urllib.request.urlopen(url).read()
    json_body = json.loads(body)
    l = list(json_body['rates'].keys())
    l.append(DEFAULT_BASE)
    return l
