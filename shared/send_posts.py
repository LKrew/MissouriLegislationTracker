from .bsky import post_to_bsky, get_client
from .twitter import send_tweet, get_twitter_client
from .mast import send_post_to_mastodon, get_mastodon_client
from .cosmos_logic import get_cosmos_client, remove_bill, get_next_bill
import logging
    
def post_bill():
    db_client = get_cosmos_client()
    bill = get_next_bill(db_client)
    if bill == None:
        return "No Bill To Post"
    newline = '\n'
    sponsors = [f"{obj['name']} ({obj['partyAffiliation']}) district {obj['district']}" for obj in bill['sponsors']]
    if len(sponsors) == 1:
        sponsor_string = f"Sponsor: {sponsors[0]}"
    else:
        sponsor_string = f"Sponsors:\n- {(f"{newline}- ").join(sponsors)}"
    body = f"{bill['number']}: {bill['title']} {newline}Status: {bill['last_action']} {bill['last_action_date']}{newline}{sponsor_string}{newline}More Info: {bill['state_link']}"
    try:
        pass
        twitter_client = get_twitter_client()
        send_tweet(body, twitter_client)
    except Exception as e : 
        logging.exception('Twitter Failed: %s', e)
    try:
        bsky_client = get_client() 
        post_to_bsky(body, bsky_client)
    except Exception as e:
        logging.exception('Blue Sky Failed: %s', e)
    try:
        pass
        mast_client = get_mastodon_client()
        send_post_to_mastodon(body, mast_client)
    except Exception as e:
        logging.exception('Mastodon Failed: %s', e)
    remove_bill(db_client, bill['id'])
    return "Run Completed"
    