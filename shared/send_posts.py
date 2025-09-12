from datetime import datetime, timezone
from shared.models.Enums import PoliticalParty
from .bsky import get_client, detailed_post_to_bsky
from .twitter import send_tweet, get_twitter_client
from .mast import send_post_to_mastodon, get_mastodon_client
from .cosmos_logic import get_cosmos_client, get_next_bill, upsert_bill
from .account_config import USAccountConfig, MOAccountConfig
import logging
from .models.Bill import Bill
import requests

def refresh_bill_data(bill: Bill, account_config):
    """Get fresh bill details from LegiScan API right before posting"""
    try:
        api_url = f"{account_config.legiscan_base_url}{account_config.legiscan_api_key}&op="
        get_bill_uri = f"{api_url}{account_config.legiscan_bill_uri}{bill.bill_id}"
        
        response = requests.get(get_bill_uri)
        if response.status_code == 200:
            fresh_bill_data = response.json()['bill']
            # Update the bill with fresh data while preserving posted status
            bill.update_from_json(fresh_bill_data)
            logging.info(f"Refreshed data for bill {bill.bill_id}")
        else:
            logging.warning(f"Failed to refresh bill {bill.bill_id}: {response.status_code}")
    except Exception as e:
        logging.error(f"Error refreshing bill {bill.bill_id}: {str(e)}")
    
    return bill
    
def post_bill(account_config):
    db_client = get_cosmos_client(account_config)
    bill = get_next_bill(db_client, account_config)
    
    if bill is None:
        return "No Bill To Post"
    bill = Bill.from_json(bill)
    logging.info(f"Running send_posts.post_bill: on bill {bill.bill_number}")
    
    # Get fresh bill details right before posting
    bill = refresh_bill_data(bill, account_config)
    
    post_to_platforms(bill, account_config)
    
    bill.posted = True
    bill.posted_date = datetime.now(timezone.utc).isoformat()
    updated_bill = bill.to_dict()
    updated_bill['id'] = str(bill.bill_id)
    upsert_bill(db_client, updated_bill)

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
        description = f'{newline}Description: {bill.description}'
    else:
        description = ""
    body = f"{bill.bill_number}: {bill.title}{description}{newline}Status: {bill.last_action} {bill.last_action_date}{newline}{sponsor_string}{newline}More Info: {most_recent_text}"
    return body

def format_us_bill_body(bill: Bill):
    newline = '\n'
    sponsor_string = get_sponsor_counts(bill.sponsors)
    bill.texts.sort(key=lambda text: text.date, reverse=True)
    if bill.description != bill.title:
        description = ""# f'{newline}Description: {bill.description}'
    else:
        description = ""
    most_recent_text = bill.texts[0].state_link if bill.texts else bill.state_link if bill.state_link else "No texts available"
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

def post_to_platforms(bill, account_config):
    
    body = format_us_bill_body(bill)
    try:
        if account_config.consumer_key:
            twitter_client = get_twitter_client(account_config)
            send_tweet(body, twitter_client)
    except Exception as e:
        logging.exception('Twitter Failed: %s', e)
    
    try:
        if account_config.bsky_user:
            bsky_client = get_client(account_config)
            detailed_post_to_bsky(bill, bsky_client, account_config)
    except Exception as e:
        logging.exception('Blue Sky Failed: %s', e)
    
    try:
        if account_config.mast_access_token:
            mast_client = get_mastodon_client(account_config)
            send_post_to_mastodon(body, mast_client)
    except Exception as e:
        logging.exception('Mastodon Failed: %s', e)
    