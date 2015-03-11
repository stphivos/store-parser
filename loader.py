__author__ = 'stphivos'

import os
import pkgutil


class ParserLoaderError(Exception):
    pass


class ParserLoader(object):
    @staticmethod
    def get_all():
        parsers = []

        path = os.path.join(os.path.dirname(__file__), "plugins")
        modules = pkgutil.iter_modules(path=[path])

        for loader, mod_name, ispkg in modules:
            loaded_mod = __import__("plugins.{0}".format(mod_name), fromlist=[mod_name])
            loaded_class = getattr(loaded_mod, mod_name.title() + "Parser")
            instance = loaded_class()
            parsers.append(instance)

        return parsers