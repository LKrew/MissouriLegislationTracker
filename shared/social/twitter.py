import tweepy
from ..helpers import split_string_into_chunks

def create_post(body):
    tweet_chunks = split_string_into_chunks(body, 280)
    return tweet_chunks

def send_tweet(body, client):
    x = 0
    tweet_body = create_post(body)
    for chunk in range(0, len(tweet_body)):
        if(chunk == 0):
            x = client.create_tweet(text = tweet_body[chunk])[0]['id']
        else:
            x = client.create_tweet(text = tweet_body[chunk], in_reply_to_tweet_id=x)[0]['id']
            
def get_twitter_client(account_config):
    consumer_key = account_config.consumer_key
    consumer_secret = account_config.consumer_secret
    access_token = account_config.access_token
    access_token_secret = account_config.access_token_secret
    
    twitter_client = tweepy.Client(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token= access_token,
        access_token_secret= access_token_secret)
    return twitter_client
