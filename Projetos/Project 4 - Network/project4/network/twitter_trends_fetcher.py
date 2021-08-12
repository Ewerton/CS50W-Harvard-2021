import tweepy

class TwitterTrend():
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

class twitter_trend_fetcher():
    
    def __init__(self):
        pass

    def get_trends_wordwide():
        # API Keys and Tokens (just for testing)
        consumer_api_key = "XDQ9mOWHNEe5bNy0uYLibxEIC"
        consumer_api_secret_key = "J2pf7FdFjKA5M6XfHdbNArx0U7X8P821xoRiYBtXQ3lj5QkEKR"
        access_token = "167528516-bVkepC5tyUsfZNxPDJb0j0l67z01J6Hq7jcRDMBa"
        access_token_secret = "ZVk8kDlun1XUXZc5d5vyVwAL0AzDrpmqfo5lHWqcU3N6i"

        # Authorization and Authentication
        auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Available Locations
        #available_loc = api.trends_available()
        trends_worldwide = api.trends_place(1) # 1 for global trends
        #br = api.trends_place(23424768) # for Brazil Trends
        trends_in_english = []
        for t in trends_worldwide[0]['trends']:
            if (isEnglish(t["name"])):
                trends_in_english.append(TwitterTrend(t["name"], t["url"]))
        return trends_in_english

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True