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

    # Subparser for the timeline command
    logging.debug("Creating the home timeline subparser")
    timeline_parser = subparsers.add_parser("home",
                                            help = "Get your own timeline")

    # Subparser for the tweet command
    logging.debug("Creating the tweet subparser")
    tweet_parser = subparsers.add_parser("tweet",
                                         help="Update your twitter status!")
    tweet_parser.add_argument("update",
                              help="Content of your post - limit 140 chars!")

    # Subparser for getting a user's timeline
    logging.debug("Creating the get subparser")
    get_parser = subparsers.add_parser("get",
                                          help="Get twitter data foruser")
    get_parser.add_argument("screen_name", help="Name of the twitter user")
    get_parser.add_argument("update_num", help="Number of posts for user",
                            nargs="?", default=5)
    return parser

def get_home_timeline(auth):
    """ Get the contents of your timeline """
    get_timeline = requests.get(TIMELINE_URL, auth=auth)
    timeline = json.dumps(get_timeline.json(), indent=4)
    return timeline

def make_tweet(update, auth):
    """ Post an update to your twitter status """
    post_tweet = requests.post(UPDATE_URL, params="status=" + update, auth=auth)
    tweet = json.dumps(post_tweet.json(), indent=4)
    return tweet

def print_screenname_tweet(dump_file):
    """Print the json formatted contents in a more human readable way

    Print out only the screen name and tweet text from the input data.
    """
    dict_output = json.loads(dump_file)
    for item in dict_output:
        print item['user']['screen_name'], item['text']

def get_user_timeline(screen_name, count, auth):
    """Get the twitter timeline of a specific user """
    user_url = SCREENNAME_URL
    user_url = user_url.format(screen_name = screen_name, count=count)
    get_user_timeline = requests.get(user_url, auth=auth)
    user_timeline = json.dumps(get_user_timeline.json(), indent=4)
    return user_timeline

def main():
    """ Main function """
    auth = authorization.authorize()

    parser = make_parser()
    logging.debug("All arguments are: {!r}".format(sys.argv[0:]))
    arguments = parser.parse_args(sys.argv[1:])
    logging.debug("After parsing arguments are: {!r}".format(arguments))
    arguments = vars(arguments)
    logging.debug("Arguments are now: {!r}".format(arguments))
    command = arguments.pop("command")

    if command == "tweet":
        update = arguments.pop("update")
        tweet = make_tweet(update, auth)
        print tweet

    elif command == "home":
        my_timeline = get_home_timeline(auth)
        print_screenname_tweet(my_timeline)

    elif command == "get":
        screen_name = arguments.pop("screen_name")
        count = arguments.pop("update_num")
        user_tl = get_user_timeline(screen_name, count, auth)
        print user_tl
#        print_screenname_tweet(user_tl)

if __name__ == "__main__":
    main()
