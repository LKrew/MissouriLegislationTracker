from datetime import datetime, timezone
import requests
import logging
from atproto import Client, client_utils, models
from .cosmos_logic import get_cosmos_client, upsert_executive_order, get_next_order
from .models.ExecutiveOrders.ExecutiveOrder import ExecutiveOrder
from .bsky import get_client
def fetch_executive_orders(api_url: str):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        logging.error(f"Failed to fetch executive orders: {e}")
        return []

def store_executive_orders(account_config):
    executive_orders_data = fetch_executive_orders(account_config.api_url)
    container = get_cosmos_client(account_config)

    for order_data in executive_orders_data:
        executive_order = ExecutiveOrder.from_json(order_data)
        if executive_order.publication_date.strftime('%Y-%m-%d') == datetime.now(timezone.utc).strftime('%Y-%m-%d'):
            upsert_executive_order(container, executive_order.to_dict())
            logging.info(f"Stored Executive Order: {executive_order.document_number}")
        logging.info(f"Skipped Executive Order (Published Before Today): {executive_order.document_number}")

def post_order(account_config):
    db_client = get_cosmos_client(account_config)
    order = get_next_order(db_client)
    
    if order is None:
        return "No Order To Post"
    order: ExecutiveOrder = ExecutiveOrder.from_json(order)
    logging.info(f"Running executive_order_handler.post_order: on order {order.document_number}")
    post_to_bsky(order, account_config)
    
    order.posted = True
    order.posted_date = datetime.now(timezone.utc).isoformat()
    updated_order = order.to_dict()
    updated_order['id'] = str(order.document_number)
    upsert_executive_order(db_client, updated_order)
    
    return "Run Completed"


def post_to_bsky(order: ExecutiveOrder, account_config):
    client = get_client(account_config)
    text_builder = client_utils.TextBuilder()
    text_builder.tag(f'{order.subtype}: {order.executive_order_number}', f'EO{order.executive_order_number}')
    text_builder.text(f'\nTitle: {order.title}\nSigned On: {order.signing_date}')
    link_embed = models.AppBskyEmbedExternal.Main(
        external = models.AppBskyEmbedExternal.External(
            title=f'{order.title}',
            description=f'{order.subtype}: {order.executive_order_number}',
            uri = order.html_url
        )
    )
    if len(text_builder.build_text()) <= 300:
        client.send_post(text_builder, embed=link_embed)
        return
# Example usage:
# account_config = AccountConfig(db_name='your_db_name', container_name='your_container_name')
# store_executive_orders('https://api.example.com/executive_orders', account_config)