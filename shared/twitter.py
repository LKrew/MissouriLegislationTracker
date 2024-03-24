import tweepy
import os
from .helpers import split_string_into_chunks

def create_post(bill):
    newline = '\n'
    body = f"{bill.number}: {bill.title} {newline}Last Action:{newline}- {bill.last_action}{newline}- {bill.last_action_date}{newline}Sponsors:{newline}- {(newline+'-').join(bill.sponsors)}{newline}{newline}More Info: {bill.state_link}"#\n{bill.text}"
    tweet_chunks = split_string_into_chunks(body, 280)
    return tweet_chunks

def send_tweet(bill):
    x = 0
    client = get_twitter_client()
    tweet_body = create_post(bill)
    for chunk in range(0, len(tweet_body)):
        if(chunk == 0):
            x = client.create_tweet(text = tweet_body[chunk])[0]['id']
        else:
            x = client.create_tweet(text = tweet_body[chunk], in_reply_to_tweet_id=x)[0]['id']
            
def get_twitter_client():
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    
    twitter_client = tweepy.Client(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token= access_token,
        access_token_secret= access_token_secret)
    return twitter_client