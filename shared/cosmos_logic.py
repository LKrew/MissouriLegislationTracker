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
    query = "SELECT c.bill_id, c.change_hash FROM c"
    bills = list(container.query_items(query=query, enable_cross_partition_query=True))
    return bills if bills else None

def upsert_bill(container, bill):
    try:
        logging.info("Uploading Bill")
        container.upsert_item(body=bill)
    except Exception as ex:
        logging.info(f"Failed to Upload {bill}")
        
def get_next_bill(db):
    query =  "SELECT TOP 1 * FROM c WHERE c.posted = false ORDER BY c.created_date ASC"
    bill = list(db.query_items(query=query, enable_cross_partition_query=True))
    if len(bill) <= 0:
        return None
    return bill[0]

def remove_bill(db, bill_id):
    try:
        logging.info(f"Deleting Item {bill_id}")
        db.delete_item(item=str(bill_id), partition_key=bill_id)
        logging.info("Successfully Deleted")
    except Exception as ex:
        logging.error(f"Failed to Delete Item {bill_id}: {ex}")