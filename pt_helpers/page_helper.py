from os import environ
import json
import urllib.request

WOT_URL = 'http://api.mywot.com/0.4/public_link_json2?hosts={}&key={}'


class NoWOTKeyException(Exception):
    pass


class Confident:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value >= 80:
            return "Really Confident"
        if self.value >= 60:
            return "Confident"
        if self.value >= 40:
            return "Not Sure"
        if self.value >= 20:
            return "Not Confident"
        if self.value >= 0:
            return "Really Not Confident"
        return "N/A"


class Reputation:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value >= 80:
            return "Excellent"
        if self.value >= 60:
            return "Good"
        if self.value >= 40:
            return "Unsatisfactory"
        if self.value >= 20:
            return "Poor"
        if self.value >= 0:
            return "Very poor"
        return "N/A"


class PageReputation:
    def __init__(self, reputation_value, confident_value):
        self.reputation = Reputation(reputation_value)
        self.confident = Confident(confident_value)

    def __str__(self):
        return "{} [{}]".format(self.reputation, self.confident)

    @classmethod
    def from_json(cls, json_body):
        if json_body:
            return cls(json_body[0], json_body[1])
        else:
            return cls(-1, -1)


class Category:
    categories = {'101': ('Negative', 'Malware or viruses'),
                  '102': ('Negative', 'Poor customer experience'),
                  '103': ('Negative', 'Phishing'),
                  '104': ('Negative', 'Scam'),
                  '105': ('Negative', 'Potentially illegal'),

                  '201': ('Questionable', 'Misleading claims or unethical'),
                  '202': ('Questionable', 'Privacy risks'),
                  '203': ('Questionable', 'Suspicious'),
                  '204': ('Questionable', 'Hate, discrimination'),
                  '205': ('Questionable', 'Spam'),
                  '206': ('Questionable', 'Potentially unwanted programs'),
                  '207': ('Questionable', 'Ads / pop-ups'),

                  '301': ('Neutral', 'Online tracking'),
                  '302': ('Neutral', 'Alternative or controversial medicine'),
                  '303': ('Neutral', 'Opinions, religion, politics'),
                  '304': ('Neutral', 'Other'),

                  '401': ('Negative', 'Adult content'),
                  '402': ('Questionable', 'Incidental nudity'),
                  '403': ('Questionable', '	Gruesome or shocking'),
                  '404': ('Positive', 'Site for kids'),

                  '501': ('Positive', 'Good site'),
                  }

    def __init__(self, category_number, confident_value):
        category = self.categories[category_number]
        self.group = category[0]
        self.description = category[1]
        self.confident = Confident(confident_value)

    def __str__(self):
        return "[{}] {} [{}]"\
            .format(self.group, self.description, self.confident)


class PageInfo:
    def __init__(self, page_url, normal_rep, kid_rep, categories):
        self.url = page_url
        self.normal_rep = normal_rep
        self.kid_rep = kid_rep
        self.categories = categories

    def __str__(self):
        return str(self.__dict__)


def wot_key():
    if 'PTH_WOT_KEY' not in environ:
        raise NoWOTKeyException
    else:
        return environ['PTH_WOT_KEY']


def base_url(url):
    splited = url.split('/')
    if splited[0] == "https:" or splited[0] == "http:":
        return splited[2]
    else:
        return splited[0]


def wot_info(page_url):
    page_url = base_url(page_url)
    url = WOT_URL.format(page_url+"/", wot_key())
    body = urllib.request.urlopen(url).read()
    json_body = json.loads(body)[page_url]
    normal_rep = PageReputation.from_json(json_body.get('0'))
    kid_rep = PageReputation.from_json(json_body.get('4'))
    categories = []
    if isinstance(json_body.get('categories'), dict):
        for x in json_body['categories'].items():
            categories.append(Category(x[0], x[1]))
    return PageInfo(page_url, normal_rep, kid_rep, categories)
