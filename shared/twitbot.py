import requests
from .bill import Bill
from .bsky import post_to_bsky
from .twitter import send_tweet
from .mast import send_post_to_mastodon
from datetime import datetime, date
import os
from dotenv import load_dotenv
import logging

def main():
    logging.info(f'Starting Run: {date.today()}')
    target_strings = ["third read", "passed", "passes", "perfect", "introduced" ]
    api_key = os.environ['LEGISCAN_API_KEY']
    api_url = f"https://api.legiscan.com/?key={api_key}&op="
    bill_id = ""
    get_bill_uri = f"getBill&id="
    bill_list = requests.get(api_url + 'getMasterList&id=2122').json()['masterlist']
    bills = []
    for b in reversed(bill_list.items()):
        if b[0] == 'session': continue
        bill = Bill.from_json(b[1])
        bill_id = bill.bill_id
        if(datetime.strptime(bill.last_action_date, '%Y-%m-%d').date() == date.today()):
            for target_string in target_strings:
                if target_string in bill.last_action.lower():  
                    response = requests.get(api_url + get_bill_uri + str(bill_id))
                    if response.status_code == 200:
                        bill_details = response.json()['bill']
                        bill.state_link = bill_details['state_link']
                        bill.sponsors = [f"{person['name']} of District {person['district']} ({person['party']})" for person in bill_details['sponsors']]
                        bills.append(bill)
    bills = sorted(bills, key=lambda x: x.last_action_date)
    print(len(bills))
    logging.info(f'Todays Bills: {len(bills)}')
    for bill in bills:
        try:
            logging.info("Posting to Twitter")
            send_tweet(bill)
        except:
            logging.exception("Failed to Post to Twitter/X")
        try: 
            logging.info("Posting to Bsky")
            post_to_bsky(bill)
        except:
            logging.exception("Failed to Post to Blue Sky")
        try:
            logging.info("Posting to Mastodon")
            send_post_to_mastodon(bill)
        except:
            logging.exception("Failed to Post to Mastodon")
    logging.info("Completed Run")
## Commented out for Azure Funtion Deployment, Uncomment to run via Bash Script
if __name__ == "__main__":
    load_dotenv('.env')
    print(datetime.strftime(date.today(), '%Y-%m-%d'))
    main()    