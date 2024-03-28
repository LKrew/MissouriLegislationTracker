import logging
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import os

def get_cosmos_client():
    db_client = cosmos_client.CosmosClient(os.environ['ACCOUNT_HOST'], os.environ['ACCOUNT_KEY'])
    try: 
        database = db_client.create_database(os.environ["COSMOS_DATABASE"])
        logging.info("Databse Created")
    except exceptions.CosmosResourceExistsError:
        logging.info("Database Already Exists Connecting to Db")
        database = db_client.get_database_client(os.environ["COSMOS_DATABASE"])
    try:
        container = database.create_container(
            id = os.environ["COSMOS_CONTAINER"],
            partition_key=PartitionKey(path='/id'),
            offer_throughput=400
        )
        logging.info("Container Created Successfully")
    except exceptions.CosmosResourceExistsError:
        logging.info("Container Already Exists Connecting to Existing Container")
        container = database.get_container_client(os.environ["COSMOS_CONTAINER"])
    return container

def upsert_bill(container, bill):
    try:
        logging.info("Uploading Bill")
        container.upsert_item(body=bill)
    except Exception as ex:
        logging.info(f"Failed to Upload {bill}")
        
def get_next_bill(db):
    query =  "SELECT TOP 1 * FROM c ORDER BY c.created_date ASC"
    bill = list(db.query_items(query=query, enable_cross_partition_query=True))
    if len(bill) <= 0:
        return None
    return bill[0]

def remove_bill(db, bill_id):
    try:
        logging.info(f"Deleting Item {bill_id}")
        db.delete_item(item=bill_id, partition_key=bill_id)
        logging.info("Successfully Deleted")
    except:
        logging.info(f"Failed to Delete Item {bill_id}")