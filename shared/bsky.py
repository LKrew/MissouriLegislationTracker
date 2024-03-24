from atproto import Client, client_utils, models
import os
from .helpers import split_string_into_chunks
import re


def create_post(text_chunk):
    text_builder = client_utils.TextBuilder()
    newline = '\n'
    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    matches = list(re.finditer(url_pattern, text_chunk))
    partial_chunks = []
    start = 0
    for match in matches:
        url = match.group()
        end = match.start()
        partial_chunks.append(text_chunk[start:end])
        partial_chunks.append(url)
        start = match.end()
    if len(partial_chunks) == 0:
        text_builder.text(text_chunk)
        return text_builder
    for chunk in partial_chunks:
        if re.search(url_pattern, chunk):
            text_builder.link(chunk, chunk)
        else:
            text_builder.text(chunk)
    return text_builder

def post_to_bsky(bill):
    newline = '\n'
    client = get_client()
    body = f"{bill.number}: {bill.title} {newline}Last Action:{newline}- {bill.last_action}{newline}- {bill.last_action_date}{newline}Sponsors:{newline}- {(newline+'- ').join(bill.sponsors)}{newline}{newline}More Info: {bill.state_link}"
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

def get_client():
    bsky_client = Client()
    bsky_client.login(
        os.environ['BSKY_USER']#'molegtracker.bsky.social'
        , os.environ['BSKY_PASSWORD']#'Lkrew005!'
        )
    return bsky_client