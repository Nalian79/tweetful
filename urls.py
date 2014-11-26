API_URL = "https://api.twitter.com"
REQUEST_TOKEN_URL = API_URL + "/oauth/request_token"
AUTHORIZE_URL = API_URL + "/oauth/authorize?oauth_token={request_token}"
ACCESS_TOKEN_URL = API_URL + "/oauth/access_token"
TIMELINE_URL = API_URL + "/1.1/statuses/home_timeline.json"
UPDATE_URL = API_URL + "/1.1/statuses/update.json"
SCREENNAME_URL = API_URL + \
    "/1.1/statuses/user_timeline.json?={screen_name}=twitterapi&count={count}"
