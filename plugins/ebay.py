__author__ = 'stphivos'

from parsing import Parser, HtmlTraversal
from query import Result


class EbayParser(Parser):
    def __init__(self):
        super().__init__("ebay", "www.ebay.com", "/sch/i.html?_skc=100", "_nkw", "_pgn")

    def extract_page_count(self, markup):
        count = 1

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("a", {"class": "pg", "aria-labelledby": "pag-lbl"})

        if len(elements) > 0:
            count = int(traverse.in_element(elements[-1]).get_value())

        return count

    def extract_results(self, markup):
        results = []

        traverse = HtmlTraversal(markup)
        elements = traverse.get_elements("li", {"class": "sresult"})

        for x in elements:
            result = Result()
            result.title = traverse.in_element(x).get_value_of("a", {"class": "vip"})
            result.url = traverse.in_element(x).get_attr_of("a", {"class": "vip"}, "href")
            result.price = traverse.in_element(x).get_value_of("span", {"class": "bold"})
            results.append(result)

        return results