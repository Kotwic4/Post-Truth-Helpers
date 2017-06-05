import webbrowser

GOOGLE_URL = "https://www.google.{}/#safe={}&q={}"
DUMMIES_URL = "http://lmgtfy.com/?q={}"


def search(query, tld='com', safe='off'):
    url = GOOGLE_URL.format(tld, safe, query)
    webbrowser.open(url)


def dummies_search(query):
    url = DUMMIES_URL.format(query)
    webbrowser.open(url)
