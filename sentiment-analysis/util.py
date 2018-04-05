import json
import re


def read_json(file_name):
    with open('config/' + file_name, encoding="utf-8") as f:
        return json.load(f)


def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())