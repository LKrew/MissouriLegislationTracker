from asyncio import sleep
import requests
from .models.Bill import Bill
from .account_config import AccountConfig
from .cosmos_logic import get_all_bill_states, get_cosmos_client, upsert_bill,get_bill_by_id
from datetime import datetime, date, timedelta
import logging

def main(account_config):
    logging.info(f'Starting Run: {date.today()}')
    api_url = f"{account_config.legiscan_base_url}{account_config.legiscan_api_key}&op="
    session_id = get_latest_session_id(api_url, account_config)
    bills = get_bills_for_today(api_url, session_id, account_config)
    logging.info(f'Updating Bills: {len(bills)}')
    process_bills(bills, account_config)

def get_latest_session_id(api_url, account_config):
    """Get the latest session ID from the LegiScan API"""
    get_session_list_uri = f"{api_url}{account_config.legiscan_session_uri}{account_config.legiscan_state_id}"
    sessions = requests.get(get_session_list_uri).json()
    return sessions['sessions'][0]['session_id']

def get_bills_for_today(api_url, session_id, account_config):
    """Get the bills for today from the LegiScan API"""
    db_container = get_cosmos_client(account_config)
    get_bill_list_uri = f'{api_url}{account_config.legiscan_masterlist_uri}{session_id}'
    bill_list = requests.get(get_bill_list_uri).json()['masterlist']
    bills = []
    
    bill_states = get_all_bill_states(db_container)
    
    last_action_dict = {}
    change_hash_dict = {}
    if bill_states:
        change_hash_dict = {bill['bill_id']: bill['change_hash'] for bill in bill_states}
        last_action_dict = {bill['bill_id']: bill['last_action'] for bill in bill_states}
    
    for b in reversed(bill_list.items()):
        if b[0] == 'session':
            continue
        
        current_bill = Bill.from_json(b[1])
        
        # Check if bill has new action (needs a post)
        needs_post = (
            current_bill.bill_id not in last_action_dict or
            last_action_dict[current_bill.bill_id] != current_bill.last_action
        )
        
        if needs_post:
            # Just store basic bill info - detailed refresh happens at post time
            current_bill.posted = False
            current_bill.posted_date = None
            bills.append(current_bill)
    
    return bills

def is_bill_relevant_today(bill, account_config):
    """
    Check if a bill is relevant for posting today
    UNUSED AS OF NOW
    """
    try:
        if datetime.strptime(bill.last_action_date, '%Y-%m-%d').date() == date.today():
            if any(target in bill.last_action for target in account_config.target_actions):
                if not any(excluded in bill.last_action for excluded in account_config.excluded_actions):
                    return True
    except Exception as e:
        logging.info(f'Error Processing Bill: {bill.bill_id}')
    return False

def get_bill_details(api_url, bill_id, account_config):
    """Get the details of a bill from the LegiScan API"""
    get_bill_uri = f"{api_url}{account_config.legiscan_bill_uri}{bill_id}"
    response = requests.get(get_bill_uri)
    if response.status_code == 200:
        return response.json()['bill']
    return None

def process_bills(bills, account_config):
    """Process the bills and upload them to the database"""
    logging.info(f'Todays Bills: {len(bills)}')
    db_container = get_cosmos_client(account_config)
    for bill in bills:
        #if is_bill_relevant_today(bill, account_config):
        bill.created_date = datetime.now()
        bill_dict = bill.to_dict()
        bill_dict['id'] = str(bill_dict['bill_id'])
        upsert_bill(db_container, bill_dict)
        count = 0
        if(count % 50 == 0):
            sleep(1)