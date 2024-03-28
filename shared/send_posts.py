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
    body = f"{bill['number']}: {bill['title']} {newline}Last Action:{newline}- {bill['last_action']}{newline}- {bill['last_action_date']}{newline}Sponsors:{newline}- {(newline+'- ').join(sponsors)}{newline} {newline}More Info: {bill['state_link']}"
    
    twitter_client = get_twitter_client()
    mast_client = get_mastodon_client()
    bsky_client = get_client()
    
    try:
        send_tweet(body, twitter_client)
    except:
        logging.exception("Failed to Post to Twitter/X")
    try: 
        post_to_bsky(body, bsky_client)
    except:
        logging.exception("Failed to Post to Blue Sky")
    try:
        send_post_to_mastodon(body, mast_client)
    except:
        logging.exception("Failed to Post to Mastodon")
    remove_bill(db_client, bill['id'])
    return "Run Completed"
    