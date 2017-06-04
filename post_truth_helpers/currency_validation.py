import urllib.request
import json


class CurrencyValidation:
    def generate_url(self, rate, base="USD", date="latest"):
        return "http://api.fixer.io/{}?base={}&symbols={}".format(date, base, rate)

    def download_rate(self, rate, base="USD", date="latest"):
        url = self.generate_url(rate, base, date)
        body = ""
        try:
            body = urllib.request.urlopen(url).read()
        except urllib.error.URLError as e:
            body = e.read()
            l = json.loads(body)
            raise self.MyError(l['error'])
        return body

    def test(self, rate, base="USD", date="latest"):
        try:
            print(self.download_rate('EURO', 'PLN', '2016-13-11'))
        except self.MyError as e:
            print(e)

    class MyError(Exception):
        pass

validator = CurrencyValidation()
validator.test('EURO','PLN','2016-13-11')
generate_url('EURO','PLN','2017-06')
download_rate('EURO','PLN','2016-13-11')
from os import environ
environ["TEST"] = "1"
environ["TEST"]

import urllib.request
s = urllib.request.urlopen("http://api.fixer.io/latest?symbols=bla&base=USD").read()
l = json.loads(s)
l['rates']

l = json.loads('{"base":"USD","date":"2017-06-01","rates":{"AUD":1.3532,"BGN":1.7433,"BRL":3.2209,"CAD":1.3508,"CHF":0.97005,"CNY":6.8089,"CZK":23.529,"DKK":6.6311,"GBP":0.77752,"HKD":7.792,"HRK":6.6075,"HUF":274.13,"IDR":13310.0,"ILS":3.5511,"INR":64.466,"JPY":111.0,"KRW":1121.7,"MXN":18.647,"MYR":4.288,"NOK":8.4584,"NZD":1.4146,"PHP":49.716,"PLN":3.7285,"RON":4.0721,"RUB":56.63,"SEK":8.7138,"SGD":1.3838,"THB":34.15,"TRY":3.54,"ZAR":13.05,"EUR":0.89135}}')
l['base']

import json
def as_complex(dct):
    print(dct['base'])
    return dct

json.loads('{"base":"USD","date":"2017-06-01","rates":{"bla":"bla"}}')
