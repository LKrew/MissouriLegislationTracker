from datetime import datetime, timezone
from shared.models.Enums import PoliticalParty
from .bsky import post_to_bsky, get_client
from .twitter import send_tweet, get_twitter_client
from .mast import send_post_to_mastodon, get_mastodon_client
from .cosmos_logic import get_cosmos_client, remove_bill, get_next_bill, upsert_bill
from .account_config import USAccountConfig, MOAccountConfig
import logging
from .models.Bill import Bill
    
def post_bill(account_config):
    db_client = get_cosmos_client(account_config)
    bill = get_next_bill(db_client)
    
    if bill is None:
        return "No Bill To Post"
    bill = Bill.from_json(bill)
    if isinstance(account_config, USAccountConfig):
        body = format_us_bill_body(bill)
    elif isinstance(account_config, MOAccountConfig):
        body = format_state_bill_body(bill)
    else:
        raise ValueError("Unsupported account configuration")
    
    post_to_platforms(body, account_config)
    
    bill.posted = True
    bill.posted_date = datetime.now(timezone.utc).isoformat()
    updated_bill = bill.to_dict()
    updated_bill['id'] = str(bill.bill_id)
    upsert_bill(db_client, updated_bill)
    #no longer deleting
    #remove_bill(db_client, bill.bill_id)
    return "Run Completed"

def format_state_bill_body(bill: Bill):
    newline = '\n'
    sponsors = [f"{obj.person.name} ({obj.person.party[0]}) district {obj.person.district}" for obj in bill.sponsors]
    if len(sponsors) == 1:
        sponsor_string = f"Sponsor: {sponsors[0]}"
    else:
        sponsor_string = f"Sponsors:{newline}- {(f'{newline}- ').join(sponsors)}"
    bill.texts.sort(key=lambda text: text.date, reverse=True)
    most_recent_text = bill.texts[0].state_link if bill.texts else bill.state_link if bill.state_link else "No texts available"
    if bill.description != bill.title:
        description = f'{newline}Description: {description}'
    else:
        description = ""
    body = f"{bill.bill_number}: {bill.title}{description}{newline}Status: {bill.last_action} {bill.last_action_date}{newline}{sponsor_string}{newline}More Info: {most_recent_text}"
    return body

def format_us_bill_body(bill: Bill):
    newline = '\n'
    sponsor_string = get_sponsor_counts(bill.sponsors)
    bill.texts.sort(key=lambda text: text.date, reverse=True)
    if bill.description:
        if bill.description != bill.title:
            description = f'{newline}Description: {description}'
        else:
            description = ""
    else:
        description = ""
    most_recent_text = bill.texts[0].state_link if bill.texts else "No texts available"
    body = f"{bill.bill_number}: {bill.title}{description}{newline}Status: {bill.last_action} {bill.last_action_date}{newline}{sponsor_string}{newline}More Info: {most_recent_text}"
    return body

def get_sponsor_counts(sponsors):
    party_counts = {
        PoliticalParty.REPUBLICAN.name: 0,
        PoliticalParty.DEMOCRAT.name: 0,
        PoliticalParty.INDEPENDENT.name: 0,
        PoliticalParty.LIBERTARIAN.name: 0,
        PoliticalParty.GREEN_PARTY.name: 0,
        PoliticalParty.NONPARTISAN.name: 0,
        'OTHER': 0
    }
    total = len(sponsors)
    for sponsor in sponsors:
        party = sponsor.person.party
        if party in party_counts:
            party_counts[party] += 1
        else:
            party_counts['OTHER'] += 1
            
    party_counts_list = []
    
    for party, count in party_counts.items():
        if count > 0:
            party_counts_list.append((count, party))
    newline = '\n'
    party_counts_list.sort(reverse=True, key=lambda x: x[0])
    party_counts = f'{newline}- '.join([f'{party.title()}: {count}' for count, party in party_counts_list])
    
    sponsor_string = f'Sponsors:{newline}- {party_counts}'
    return sponsor_string

def post_to_platforms(body, account_config):
    try:
        if account_config.consumer_key:
            twitter_client = get_twitter_client(account_config)
            send_tweet(body, twitter_client)
    except Exception as e:
        logging.exception('Twitter Failed: %s', e)
    
    try:
        if account_config.bsky_user:
            bsky_client = get_client(account_config)
            post_to_bsky(body, bsky_client)
    except Exception as e:
        logging.exception('Blue Sky Failed: %s', e)
    
    try:
        if account_config.mast_access_token:
            mast_client = get_mastodon_client(account_config)
            send_post_to_mastodon(body, mast_client)
    except Exception as e:
        logging.exception('Mastodon Failed: %s', e)
    