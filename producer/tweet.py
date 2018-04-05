class Tweet(object):
    def __init__(self, raw):
        self.id = raw['id']
        self.text = raw['text']
        self.created_at = raw['created_at']
