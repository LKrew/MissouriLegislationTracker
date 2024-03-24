from mastodon import Mastodon
from .helpers import split_string_into_chunks
import os
def get_mastodon_client():
    mast_client_id = os.environ['MAST_CLIENT_ID']
    mast_client_secret = os.environ['MAST_CLIENT_SECRET']
    mast_access_token = os.environ['MAST_ACCESS_TOKEN']
    mastodon = Mastodon(
        client_id = mast_client_id,
        client_secret = mast_client_secret,
        access_token = mast_access_token,
        api_base_url='https://mastodon.social')
    return mastodon

def create_post(bill):
    newline = '\n'
    tab = '\t'
    body = f"{bill.number}: {bill.title} {newline}Last Action:{newline}- {bill.last_action}{newline}- {bill.last_action_date}{newline}Sponsors:{newline}- {(newline+'- ').join(bill.sponsors)}{newline}{newline}More Info: {bill.state_link}"
    post_chunks = split_string_into_chunks(body, 500)
    return post_chunks

def send_post_to_mastodon(bill):
    x = 0
    client = get_mastodon_client()
    post_body = create_post(bill)
    for chunk in range(0, len(post_body)):
        if(chunk == 0):
            x = client.status_post(post_body[chunk])
        else:
            x = client.status_post(post_body[chunk], in_reply_to_id=x['id'])
