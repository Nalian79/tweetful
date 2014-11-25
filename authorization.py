import urlparse

import requests
from requests_oauthlib import OAuth1

from secret import CLIENT_KEY, CLIENT_SECRET
from urls import *

def get_request_token():
    """ Get a token allowing us to request user authorization """
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET)
    response = requests.post(REQUEST_TOKEN_URL,
                             auth=oauth)
    credentials = urlparse.parse_qs(response.content)

    request_token = credentials.get("oauth_token")[0]
    request_secret = credentials.get("oauth_token_secret")[0]
    return request_token, request_secret


def authorize():
    """ A complete OAuth authentication flow """
    request_token, request_secret = get_request_token()
    print request_token, request_secret
