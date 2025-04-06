
import sys
import os
import logging
import time
from sqlalchemy.exc import IntegrityError
from sqlalchemy import not_

from sp_api.api import Orders
from sp_api.base import Marketplaces, SellingApiException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.connect import SessionLocal
from db.models import AmazonOrderDetail, AmazonOrderDetailItem
from client_config import CREDENTIALS as credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = SessionLocal()

marketplace_region_map = {
    "North America": [Marketplaces.US, Marketplaces.CA, Marketplaces.MX],
    "Europe": [Marketplaces.DE, Marketplaces.FR, Marketplaces.IT, Marketplaces.ES,
               Marketplaces.NL, Marketplaces.BE, Marketplaces.SE, Marketplaces.PL,
               Marketplaces.TR, Marketplaces.UK],
    "Far East": [Marketplaces.JP],
    "Australia": [Marketplaces.AU],
}

def get_unfetched_order_ids(limit=100):
    subquery = session.query(AmazonOrderDetailItem.order_id).distinct()
    orders = session.query(AmazonOrderDetail).filter(
        not_(AmazonOrderDetail.amazon_order_id.in_(subquery))
    ).limit(limit).all()
    return orders

def fetch_order_items(order_id, creds, marketplace):
    try:
        api = Orders(credentials=creds, marketplace=marketplace)
        res = api.get_order_items(order_id)
        return res.payload.get("OrderItems", [])
    except SellingApiException as e:
        logger.warning(f"QuotaExceeded or API error on order {order_id}: {e}")
        time.sleep(60)
        return fetch_order_items(order_id, creds, marketplace)
    except Exception as e:
        logger.error(f"Unexpected error on {order_id}: {e}")
        return []

def insert_items(order_id, items, country):
    inserted = 0
    objects = []
    for item in items:
        try:
            qty = item.get("QuantityOrdered", 1)
            item_price = item.get("ItemPrice", {}).get("Amount")
            unit_price = float(item_price) / qty if item_price and qty else None

            obj = AmazonOrderDetailItem(
                order_id=order_id,
                asin=item.get("ASIN"),
                seller_sku=item.get("SellerSKU"),
                title=item.get("Title"),
                quantity_ordered=qty,
                item_price=item_price,
                item_currency=item.get("ItemPrice", {}).get("CurrencyCode"),
                shipping_price=item.get("ShippingPrice", {}).get("Amount"),
                shipping_currency=item.get("ShippingPrice", {}).get("CurrencyCode"),
                country=country,
                unit_price=unit_price
            )
            objects.append(obj)
        except Exception as e:
            logger.warning(f"Skipping item in order {order_id} due to error: {e}")
            continue
    session.bulk_save_objects(objects)
    session.commit()
    return len(objects)

def get_marketplace_by_id(marketplace_id):
    for region, mks in marketplace_region_map.items():
        for m in mks:
            if m.marketplace_id == marketplace_id:
                return m, region
    return None, None

def main():
    total_inserted = 0
    while True:
        orders = get_unfetched_order_ids()
        if not orders:
            logger.info("🟢 No more orders to fetch. Exiting.")
            break

        logger.info(f"📦 Found {len(orders)} orders without items.")
        for order in orders:
            marketplace, region = get_marketplace_by_id(order.marketplace_id)
            if not marketplace or region not in credentials:
                logger.warning(f"Skipping order {order.amazon_order_id}: unknown marketplace or missing creds.")
                continue

            creds = credentials[region]
            logger.info(f"📦 Fetching items for order {order.amazon_order_id} in {marketplace.name}")
            items = fetch_order_items(order.amazon_order_id, creds, marketplace)
            inserted = insert_items(order.amazon_order_id, items, country=marketplace.name)
            logger.info(f"✅ Inserted {inserted} items for order {order.amazon_order_id}")
            total_inserted += inserted
            time.sleep(1)

        logger.info("🕒 Sleeping for a bit before next batch...")
        time.sleep(3)

    logger.info(f"🎉 Done. Total items inserted: {total_inserted}")

if __name__ == "__main__":
    main()
