from atproto import Client, client_utils, models
from .account_config import AccountConfig, MOAccountConfig, USAccountConfig
import os
from .helpers import split_string_into_chunks
import re


def create_post(text_chunk):
    text_builder = client_utils.TextBuilder()
    newline = '\n'
    url_pattern = r"(?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])"
    hashtag_pattern = r"#\w+"
    result = re.split(f'({hashtag_pattern}|{url_pattern})', text_chunk)
    result = [item for item in result if item]
    for chunk in result:
        if re.search(url_pattern, chunk):
            text_builder.link(chunk, chunk)
        elif re.search(hashtag_pattern, chunk):
            text_builder.tag(chunk, chunk[1:])
        else:
            text_builder.text(chunk)
    return text_builder

def post_to_bsky(body, client):
    chunks = split_string_into_chunks(body, 300)
    parent = ''
    root = ''
    for chunk in range(0, len(chunks)):
        post = create_post(chunks[chunk])
        if chunk == 0:
            root = models.create_strong_ref(client.send_post(post))
            parent = models.create_strong_ref(root)
        else:
            parent = models.create_strong_ref(client.send_post(
                post,
                reply_to= models.AppBskyFeedPost.ReplyRef(parent=parent, root=root)
                ))
            root = parent

def get_client(account_config):
    bsky_client = Client()
    bsky_client.login(
        account_config.bsky_user#'molegtracker.bsky.social'
        , account_config.bsky_password#'Lkrew005!'
        )
    return bsky_client