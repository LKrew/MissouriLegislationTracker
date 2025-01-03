from mastodon import Mastodon
from .helpers import split_string_into_chunks
import os
def get_mastodon_client(account_config):
    mastodon = Mastodon(
        client_id = account_config.mast_client_id,
        client_secret = account_config.mast_client_secret,
        access_token = account_config.mast_access_token,
        api_base_url='https://mastodon.social')
    return mastodon

def create_post(body):
    post_chunks = split_string_into_chunks(body, 500)
    return post_chunks

def send_post_to_mastodon(body, client):
    x = 0
    post_body = create_post(body)
    for chunk in range(0, len(post_body)):
        if(chunk == 0):
            x = client.status_post(post_body[chunk])
        else:
            x = client.status_post(post_body[chunk], in_reply_to_id=x['id'])
