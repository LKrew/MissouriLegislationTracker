import json
from typing import Any
import requests
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
from .bill import Bill, Sponsor
from .bsky import post_to_bsky, get_client
from .twitter import send_tweet, get_twitter_client
from .mast import send_post_to_mastodon, get_mastodon_client
from .cosmos_logic import get_cosmos_client, upsert_bill
from .CustomJSONEncoder import CustomJSONEncoder
from datetime import datetime, date
import os
from dotenv import load_dotenv
import logging

def main():
    logging.info(f'Starting Run: {date.today()}')
    target_strings = ["third read", "passed", "passes", "perfect", "introduced" ]
    api_key = os.environ['LEGISCAN_API_KEY']
    api_url = f"https://api.legiscan.com/?key={api_key}&op="
    get_session_list_uri = "getSessionList&state=MO"
    sessions = requests.get(api_url + get_session_list_uri).json()
    session_id = sessions['sessions'][0]['session_id']
    bill_id = ''
    get_bill_uri = f"getBill&id="
    get_bill_list_uri = f'getMasterList&id={session_id}'
    bill_list = requests.get(api_url + get_bill_list_uri).json()['masterlist']
    bills = []
    for b in reversed(bill_list.items()):
        if b[0] == 'session': continue
        bill = Bill.from_json(b[1])
        bill_id = bill.id
        if(datetime.strptime(bill.last_action_date, '%Y-%m-%d').date() == date.today()):
            for target_string in target_strings:
                if target_string in bill.last_action.lower():  
                    response = requests.get(api_url + get_bill_uri + str(bill_id))
                    if response.status_code == 200:
                        bill_details = response.json()['bill']
                        bill.state_link = bill_details['state_link']
                        bill.sponsors = [Sponsor(person['name'], person['party'], person['district']) for person in bill_details['sponsors']]
                        bills.append(bill)
    bills = sorted(bills, key=lambda x: x.last_action_date)
    logging.info(f'Todays Bills: {len(bills)}')
    db_container = get_cosmos_client()
    for bill in bills:
        bill.created_date = datetime.now()
        bill_dict = json.loads(json.dumps(bill.__dict__, cls=CustomJSONEncoder))
        upsert_bill(db_container, bill_dict)
       
if __name__ == "__main__":
    load_dotenv('.env')
    print(datetime.strftime(date.today(), '%Y-%m-%d'))
    main()    