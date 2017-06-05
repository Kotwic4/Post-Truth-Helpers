import webbrowser

GOOGLE_URL = "https://www.google.{}/#safe={}&q={}"
LMGTFY_URL = "http://lmgtfy.com/?q={}"


def search(query, tld='com', safe='off'):
    url = GOOGLE_URL.format(tld, safe, query)
    webbrowser.open(url)


def lmgtfy(query):
    url = LMGTFY_URL.format(query)
    webbrowser.open(url)
