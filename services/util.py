import json
import re

import time

"""
Module with some utility functions used throughout the application    
"""


def read_json(file_name):
    with open('config/' + file_name, encoding="utf-8") as f:
        return json.load(f)


def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters - used before sentiment analysis
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())


def twitter_time_to_epoch(created_at):
    return time.mktime(time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))


# get hosts config depending on deployment env (docker or local)
def get_hosts_config():
    hosts_config = read_json('hosts.json')
    env = hosts_config['env']
    return hosts_config[env]
