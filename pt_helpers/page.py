from os import environ


class NoWOTKeyException(Exception):
    pass

if 'PTH_WOT_KEY' not in environ:
    raise NoWOTKeyException
else:
    WOT_KEY = environ['PTH_WOT_KEY']
