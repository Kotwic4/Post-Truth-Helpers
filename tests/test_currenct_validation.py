import pytest
import pt_helpers.currency_helper as currency


def test_get_currency_rate():
    currency_rate = currency.get_rate('PLN', date='2017-06-02')
    assert isinstance(currency_rate, currency.CurrencyRate)
    assert currency_rate.base == 'USD'
    assert currency_rate.date == "2017-06-02"
    assert currency_rate.currency == "PLN"
    assert currency_rate.rate == 3.7376

    currency_rate = currency.get_rate('PLN', 'EUR', '2016-05-01')
    assert isinstance(currency_rate, currency.CurrencyRate)
    assert currency_rate.base == 'EUR'
    assert currency_rate.date == "2016-04-29"
    assert currency_rate.currency == "PLN"
    assert currency_rate.rate == 4.3965

    with pytest.raises(currency.InvalidDateException):
        currency.get_rate('PLN', date='2017-13-02')

    with pytest.raises(currency.CurrencyNotFoundException):
        currency.get_rate('P', date='2017-06-02')

    with pytest.raises(currency.InvalidBaseException):
        currency.get_rate('PLN', 'P', '2017-06-02')


def test_calculate_exchange():
    amount = currency.calculate_exchange('PLN', 10, date='2017-06-02')
    assert amount == 37.376

    amount = currency.calculate_exchange('PLN', 10, 'EUR', '2016-05-01')
    assert amount == 43.965

    amount = currency.calculate_exchange(
                                            ['PLN', 'USD'],
                                            10,
                                            'EUR',
                                            '2016-05-01')
    assert amount == 11.4045

    with pytest.raises(currency.InvalidDateException):
        currency.calculate_exchange('PLN', 10, date='2017-13-02')

    with pytest.raises(currency.CurrencyNotFoundException):
        currency.calculate_exchange('P', 10, date='2017-06-02')

    with pytest.raises(currency.InvalidBaseException):
        currency.calculate_exchange('PLN', 10, 'P', '2017-06-02')


def test_currency_list():
    assert currency.currency_list() == [
                                        'AUD',
                                        'BGN',
                                        'BRL',
                                        'CAD',
                                        'CHF',
                                        'CNY',
                                        'CZK',
                                        'DKK',
                                        'GBP',
                                        'HKD',
                                        'HRK',
                                        'HUF',
                                        'IDR',
                                        'ILS',
                                        'INR',
                                        'JPY',
                                        'KRW',
                                        'MXN',
                                        'MYR',
                                        'NOK',
                                        'NZD',
                                        'PHP',
                                        'PLN',
                                        'RON',
                                        'RUB',
                                        'SEK',
                                        'SGD',
                                        'THB',
                                        'TRY',
                                        'ZAR',
                                        'EUR',
                                        'USD',
                                        ]


def test_check_exchange():
    assert not currency.check_exchange('PLN', 10, 100)

    assert currency.check_exchange('PLN', 10, 50, 'EUR', '2016-05-01')
