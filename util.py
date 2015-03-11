__author__ = 'stphivos'

import re


def strip_text(text):
    result = text.strip("\\r \\n \\t")
    result = re.sub(r"(\\r|\\n|\\t){2,}", " ", result)
    return result


def strip_float(text):
    result = strip_text(text).replace("$", "").replace(",", "")
    try:
        return float(result)
    except ValueError:
        return float('nan')