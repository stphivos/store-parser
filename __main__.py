__author__ = 'stphivos'

import sys
import getopt
import argparse
from query import Query
from loader import ParserLoader, ParserLoaderError


def usage():
    parser = argparse.ArgumentParser(prog='StoreParser')
    parser.add_argument('q', nargs='+', help='queries stores with supplied term')
    parser.print_help()


def get_parsers():
    try:
        parsers = ParserLoader.get_all()
    except ParserLoaderError:
        print("An error occurred while loading your parsers from the settings file.")
        sys.exit(2)
    return parsers


def get_options(argv):
    try:
        opts, args = getopt.getopt(argv, "hq:", ["help", "query="])
    except getopt.GetoptError as ex:
        print(ex)
        usage()
        sys.exit(2)
    return opts


def execute_query(parsers, term, count=5):
    print("Searching for: '{0}'...".format(term))

    query = Query(parsers)
    results = query.execute(term, count)

    if len(results) > 0:
        print("\nQuery ended with results:")
        for r in sorted(results, key=lambda res: res.price):
            print(r)
    else:
        print("No results found.")


def main(argv):
    opts = get_options(argv)

    if len(opts) > 0:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-q", "--query"):
                parsers = get_parsers()
                execute_query(parsers, arg)
    else:
        usage()
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])