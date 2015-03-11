__author__ = 'stphivos'

import util


class Result(object):
    def __init__(self):
        self.title = ""
        self.__price = 0.0
        self.url = ""

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = util.strip_float(value)

    def __repr__(self):
        return "${0} - {1} at {2}".format(self.price, self.title, self.url)


class Query(object):
    def __init__(self, parsers):
        self.parsers = parsers

    def execute(self, term, count):
        results = []
        for p in self.parsers:
            items = p.search(term, count)
            for r in items:
                results.append(r)
        return results