__author__ = 'stphivos'

from parsing import Parser, HtmlTraversal
from query import Result


class AmazonParser(Parser):
    def __init__(self):
        super().__init__("amazon", "www.amazon.com", "/s?ie=UTF8", "keywords", "page")

    def extract_page_count(self, markup):
        count = 1

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("span", {"class": "pagnLink"})

        if len(elements) > 0:
            count = int(traverse.in_element(elements[-1]).get_value())

        return count

    def extract_results(self, markup):
        results = []

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("div", {"class": "a-fixed-left-grid-inner"})

        for x in elements:
            result = Result()
            result.title = traverse.in_element(x).get_value_of("h2", {"class": "s-access-title"})
            result.url = traverse.in_element(x).get_attr_of("a", {"class": "a-link-normal a-text-normal"}, "href")
            result.price = traverse.in_element(x).get_value_of("span", {"class": "a-size-base a-color-price"})
            results.append(result)

        return results