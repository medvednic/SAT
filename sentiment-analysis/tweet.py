class Tweet(object):
    def __init__(self, tweet_id, tweet_text, created_at, sentiment):
        self.id = tweet_id
        self.text = tweet_text
        self.created_at = created_at
        self.sentiment = sentiment

