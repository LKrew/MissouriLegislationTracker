from datetime import datetime
from .account_config import AccountConfig
import logging
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import os

def get_cosmos_client(account_config):
    db_client = cosmos_client.CosmosClient(os.environ['ACCOUNT_HOST'], os.environ['ACCOUNT_KEY'])
    database_name = account_config.db_name
    container_name = account_config.container_name

    try:
        database = db_client.create_database_if_not_exists(id=database_name)
        logging.info("Database created or already exists")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Failed to create or connect to database: {e}")
        raise

    try:
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path='/id'),
            offer_throughput=400
        )
        logging.info("Container created or already exists")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Failed to create or connect to container: {e}")
        raise

    return container

def get_bill_by_id(container, bill_id: str):
    query = f"SELECT * FROM c WHERE c.bill_id = {bill_id}"
    bills = list(container.query_items(query=query, enable_cross_partition_query=True))
    return bills[0] if bills else None

def get_all_bill_states(container):
    query = "SELECT c.bill_id, c.last_action, c.change_hash FROM c"
    bills = list(container.query_items(query=query, enable_cross_partition_query=True))
    return bills if bills else None

def upsert_bill(container, bill):
    logging.info(f"Upserting Bill: {bill['bill_id']}")
    try:
        logging.info("Uploading Bill")
        container.upsert_item(body=bill)
    except Exception as ex:
        logging.error(f"Failed to Upload {bill}")

def upsert_executive_order(container, order):
    logging.info(f"Upserting Executive Order: {order['document_number']}")
    try:
        logging.info("Uploading Executive Order")
        order['id'] = order['document_number']
        container.upsert_item(body=order)
    except Exception as ex:
        logging.error(f"Failed to Upload {order}")

def get_all_orders(container):
    query = "Select c.document_number FROM c"
    orders = list(container.query_items(query=query, enable_cross_partition_query=True))
    return orders

def get_next_order(db):
    query =  "SELECT TOP 1 * FROM c WHERE c.posted = false ORDER BY c.created_date ASC"
    order = list(db.query_items(query=query, enable_cross_partition_query=True))
    if len(order) <= 0:
        return None
    return order[0]

def get_next_bill(db, account_config: AccountConfig):
    query =  "SELECT * FROM c WHERE c.posted = false ORDER BY c.created_date ASC"
    bills = list(db.query_items(query=query, enable_cross_partition_query=True))
    bills = [record for record in bills if record['last_action_date'] != '0000-00-00']
    for record in bills:
        # Default priority of 6 if no match found
        priority = 6
        # Check each priority action for partial matches
        for action, action_priority in account_config.Priority_Actions.items():
            if action.lower() in record['last_action'].lower():
                priority = action_priority
                break
        record['priority'] = priority
    
    sorted_results = sorted(bills, key=lambda x: (
        x["priority"], 
        datetime.strptime(x["last_action_date"], "%Y-%m-%d")
    ))
    bill = sorted_results[0:1]  # Get the first bill with the highest priority
    
    if len(bill) <= 0:
        return None
    return bill[0]
