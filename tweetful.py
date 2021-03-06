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
    get_parser = subparsers.add_parser("get_user",
                                          help="Get twitter data foruser")
    get_parser.add_argument("screen_name", help="Name of the twitter user")
    get_parser.add_argument("update_num", help="Number of posts for user",
                            nargs="?", default=5)

    # Subparser for getting trends
    logging.debug("Creating the trends subparser")
    trend_parser = subparsers.add_parser("trends",
                                         help="Gets trending topics from twitter")
    trend_parser.add_argument("location", default=1, nargs="?",
                              help="Location for top trends")

    # Subparser for getting geo locations from twitter
    logging.debug("Creating the geoloc subparser")
    geoloc_parser = subparsers.add_parser("get_geoloc",
                                          help="ID numbers for Geo Location lookups")

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
    tweet = json.loads(tweet)
    print "You tweeted: {}".format(tweet['text'])
    print "As user: {}".format(tweet['user']['name'])
#    return tweet

def print_tweets(dump_file):
    """Print the json formatted contents in a more human readable way

    Print out only the screen name and tweet text from the input data.
    """
    dict_output = json.loads(dump_file)
    for item in dict_output:
        if 'error' in dict_output:
            print "You are not authorized to view that user's tweets."
            break
        else:
            print item['user']['screen_name'], item['text']

def get_user_timeline(screen_name, count, auth):
    """Get the twitter timeline of a specific user """
    user_url = SCREENNAME_URL
    user_url = user_url.format(screen_name = screen_name, count=count)
    get_user_timeline = requests.get(user_url, auth=auth)
    user_timeline = json.dumps(get_user_timeline.json(), indent=4)
    return user_timeline

def get_trends(geoloc, auth):
    """ Get the top trends by geo-location """
    trend_url = TRENDING_URL
    trend_url = trend_url.format(geoloc=geoloc)
    get_trends = requests.get(trend_url, auth=auth)
    get_trends_list = json.dumps(get_trends.json(), indent=4)
    trends_dict = json.loads(get_trends_list)[0]
    loc_dict = trends_dict['locations']
    for item in loc_dict:
        print "Trends for location: " + "{}".format(item['name'])
    for trend in trends_dict['trends']:
        print "Search URL: " + u"{}".format(trend['url'])
        print "Name: " + u"{}".format(trend['name'])

def get_geoloc_choices(auth):
    """ Get a list of available GeoLocations from Twitter """
    geoloc_url = GEOLOCS_URL
    get_geolocs = requests.get(geoloc_url, auth=auth)
    geoloc_list = json.dumps(get_geolocs.json(), indent=4)
    geoloc_list_of_dicts = json.loads(geoloc_list)
    geo_dict = {}
    for item in geoloc_list_of_dicts:
        geo_dict[item['name']] = item['woeid']
#        print u"Location: {!r}, id: {!r}".format(item['name'], item['woeid'])
    return geo_dict

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
    geo = get_geoloc_choices(auth)

    if command == "tweet":
        update = arguments.pop("update")
        tweet = make_tweet(update, auth)

    elif command == "home":
        my_timeline = get_home_timeline(auth)
        print_tweets(my_timeline)

    elif command == "get_user":
        screen_name = arguments.pop("screen_name")
        count = arguments.pop("update_num")
        user_tl = get_user_timeline(screen_name, count, auth)
        print_tweets(user_tl)

    elif command == "trends" or command == "get_geoloc":
        geo = get_geoloc_choices(auth)
        if command == "trends":
            geo_arg = arguments.pop("location")
            if geo_arg in geo:
                get_trends(geo[geo_arg], auth)
            else:
                print "Please provide a valid geo location, check get_geoloc"
#        get_trends(geoloc, auth)
        elif command == "get_geoloc":
            for key in geo:
                print u"{!r} : {!r}".format(key, geo[key])

if __name__ == "__main__":
    main()
