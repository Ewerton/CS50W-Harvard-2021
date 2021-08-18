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
        consumer_api_key = "w4UaFf5VGKnFWfLzyGZVP9nUn"
        consumer_api_secret_key = "8hTeBPBaOmYgCsJCcpAzNejq38yaV2pOAR5uhcfXsafiocUr8O"
        access_token = "167528516-s0Q7r45mGUEng1axnYgJWmzlyOiqoJRw7Jf71ZdK"
        access_token_secret = "I0eIAOfJmUM5ctM3xe9vZVBcHdLOlF4iG96f3YLooyxGu"

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