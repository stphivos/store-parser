__author__ = 'stphivos'

import util
import urllib.request
from lxml import html
from math import isnan
from urllib.parse import urlencode


class Parser(object):
    def __init__(self, name, host, path, key_query, key_page):
        self.name = name
        self.host = host
        self.path = path
        self.key_query = key_query
        self.key_page = key_page

    def extract_page_count(self, markup):
        raise Exception("Method extract_page_count not implemented by parser of site {0}.".format(self.host))

    def get_markup(self, term, page):
        query = urlencode({self.key_query: term, self.key_page: page})
        url = "http://{0}{1}&{2}".format(self.host, self.path, query)
        response = urllib.request.urlopen(url)
        markup = str(response.read())
        return markup

    def get_page_count(self, term):
        res = self.get_markup(term, 1)
        count = self.extract_page_count(res)
        return count

    def extract_results(self, markup):
        raise Exception("Method extract_results not implemented by parser of site {0}.".format(self.host))

    def search(self, term, count):
        results = []

        print(" -> DEBUG (get_page_count): Looking for '{0}' in {1}".format(term, self.name))
        pages = self.get_page_count(term)

        for i in range(pages):
            print(" -> DEBUG (get_markup): Fetching top {0} '{1}' results from {2}, page {3}/{4}"
                  .format(count, term, self.name, i + 1, pages))
            markup = self.get_markup(term, i + 1)
            items = self.extract_results(markup)
            for x in items[:count - len(results)]:
                if not isnan(x.price):
                    results.append(x)
            if len(results) == count:
                break
        return results


class HtmlTraversal:
    def __init__(self, markup):
        self.root = html.fromstring(markup)
        pass

    @staticmethod
    def generate_xpath(tag, attrs):
        conditions = []
        for x in attrs:
            conditions.append("contains(@{0}, '{1}')".format(x, attrs[x]))
        xpath = "//{0}[{1}]".format(tag, " and ".join(conditions))
        return xpath

    def get_elements(self, tag, attrs):
        elements = self.root.xpath(HtmlTraversal.generate_xpath(tag, attrs))
        result = [util.strip_text(html.tostring(x).decode()) for x in elements]
        return result

    def in_element(self, element):
        self.root = html.fromstring(element)
        return self

    def get_value(self):
        return util.strip_text(self.root.text_content().__str__())

    def get_attr(self, name):
        return util.strip_text(self.root.attrib[name])

    def get_value_of(self, tag, attrs):
        value = ""
        elements = self.get_elements(tag, attrs)
        if len(elements) > 0:
            value = self.in_element(elements[0]).get_value()
        return value

    def get_attr_of(self, tag, attrs, name):
        value = ""
        elements = self.get_elements(tag, attrs)
        if len(elements) > 0:
            value = self.in_element(elements[0]).get_attr(name)
        return value