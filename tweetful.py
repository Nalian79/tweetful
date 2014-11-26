import argparse
import authorization
import logging
import sys

from urls import *

import json
import requests

logging.basicConfig(filename="output.log", level=logging.DEBUG)

def make_parser():
    """ Construct the command line parser """
    logging.info("Constructing parser")
    description = "Utilize twitter from the command line"
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the tweet command
    logging.debug("Creating the tweet subparser")
    tweet_parser = subparsers.add_parser("tweet",
                                         help="Update your twitter status!")
    tweet_parser.add_argument("update", 
                              help="Content of your post - limit 140 chars!")
    return parser

def tweet(update):
    """Post an update to a twitter timeline """
    pass

def main():
    """ Main function """
    auth = authorization.authorize()

    parser = make_parser()
    logging.debug("All arguments are: {!r}".format(sys.argv[0:]))
    arguments = parser.parse_args(sys.argv[1:])
    logging.debug("After parsing arguments are: {!r}".format(arguments))
    command = arguments.pop("command")
    arguments = vars(arguments)
    logging.debug("Arguments are now: {!r}".format(arguments))
#    response = requests.get(TIMELINE_URL, auth=auth)
#    print json.dumps(response.json(), indent=4)

    if command == "tweet":
        pass


if __name__ == "__main__":
    main()
