import sys
import os
import logging
import time
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import pytz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client_config import CREDENTIALS as credentials
from sp_api.api import Orders
from sp_api.base import Marketplaces, SellingApiException
from db.connect import SessionLocal
from db.models import AmazonOrderDetail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

marketplace_timezones = {
    Marketplaces.US: "America/Los_Angeles",
    Marketplaces.CA: "America/Los_Angeles",
    Marketplaces.MX: "America/Mexico_City",
    Marketplaces.DE: "Europe/Berlin",
    Marketplaces.FR: "Europe/Paris",
    Marketplaces.IT: "Europe/Rome",
    Marketplaces.ES: "Europe/Madrid",
    Marketplaces.NL: "Europe/Amsterdam",
    Marketplaces.BE: "Europe/Brussels",
    Marketplaces.SE: "Europe/Stockholm",
    Marketplaces.PL: "Europe/Warsaw",
    Marketplaces.TR: "Europe/Istanbul",
    Marketplaces.UK: "Europe/London",
    Marketplaces.JP: "Asia/Tokyo",
    Marketplaces.AU: "Australia/Sydney"
}

session = SessionLocal()

def get_latest_order_date():
    latest = session.query(func.max(AmazonOrderDetail.purchase_date)).scalar()
    return latest or datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(days=720)

def fetch_and_insert_orders(marketplace, creds, start_date):
    logger.info(f"Fetching orders for {marketplace.name} starting from {start_date.isoformat()}")
    api = Orders(credentials=creds, marketplace=marketplace)
    next_token = None
    retry_count = 0
    total_inserted = 0

    while True:
        try:
            if next_token:
                res = api.get_orders(NextToken=next_token)
            else:
                res = api.get_orders(
                    CreatedAfter=start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    MarketplaceIds=[marketplace.marketplace_id],
                    MaxResultsPerPage=100
                )

            orders = res.payload.get('Orders', [])
            if not orders:
                break

            inserted = insert_orders(orders)
            logger.info(f"Inserted {inserted} orders for {marketplace.name} in this batch")
            total_inserted += inserted

            next_token = res.payload.get('NextToken')
            if not next_token:
                break

            time.sleep(2)

        except SellingApiException as e:
            if 'QuotaExceeded' in str(e):
                retry_count += 1
                wait_time = min(60 * retry_count, 300)
                logger.warning(f"QuotaExceeded. Sleeping {wait_time}s and retrying... [Attempt {retry_count}]")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"SP API Exception: {e}")
                break
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            break

    return total_inserted

def insert_orders(order_list):
    inserted = 0
    for order in order_list:
        try:
            obj = AmazonOrderDetail(
                amazon_order_id=order.get('AmazonOrderId'),
                purchase_date=order.get('PurchaseDate'),
                order_status=order.get('OrderStatus'),
                buyer_name=order.get('BuyerInfo', {}).get('BuyerName'),
                buyer_email=order.get('BuyerInfo', {}).get('BuyerEmail'),
                marketplace_id=order.get('MarketplaceId'),
                order_total=order.get('OrderTotal', {}).get('Amount'),
                currency=order.get('OrderTotal', {}).get('CurrencyCode'),
            )
            session.add(obj)
            session.commit()
            inserted += 1
        except IntegrityError:
            session.rollback()
    return inserted

def verify_recent_orders():
    last_10_min = datetime.utcnow() - timedelta(minutes=10)
    rows = session.query(AmazonOrderDetail).filter(
        AmazonOrderDetail.purchase_date >= last_10_min
    ).all()
    logger.info(f"🟢 {len(rows)} orders inserted in the last 10 minutes.")
    if rows:
        logger.info("📋 Sample order:")
        sample = rows[0]
        logger.info(f"  ID: {sample.amazon_order_id}, Status: {sample.order_status}, Date: {sample.purchase_date}")

def main():
    latest_date = get_latest_order_date()
    logger.info(f"Starting sync from {latest_date.isoformat()}")

    total_all = 0
    for marketplace, tz_str in marketplace_timezones.items():
        local_tz = pytz.timezone(tz_str)
        start_date = latest_date.astimezone(local_tz)
        creds = credentials.get(_region_label(marketplace), None)
        if not creds:
            logger.warning(f"No credentials for {marketplace.name}. Skipping.")
            continue
        try:
            inserted = fetch_and_insert_orders(marketplace, creds, start_date)
            logger.info(f"✅ {inserted} total inserted for {marketplace.name}")
            total_all += inserted
        except Exception as e:
            logger.error(f"❌ Error syncing {marketplace.name}: {e}")

    logger.info(f"🎉 Sync complete. Total inserted: {total_all}")
    verify_recent_orders()

def _region_label(marketplace):
    if marketplace in [Marketplaces.US, Marketplaces.CA, Marketplaces.MX]:
        return "North America"
    elif marketplace in [Marketplaces.DE, Marketplaces.FR, Marketplaces.IT, Marketplaces.ES,
                         Marketplaces.NL, Marketplaces.BE, Marketplaces.SE, Marketplaces.PL,
                         Marketplaces.TR, Marketplaces.UK]:
        return "Europe"
    elif marketplace == Marketplaces.JP:
        return "Far East"
    elif marketplace == Marketplaces.AU:
        return "Australia"
    else:
        return None

if __name__ == "__main__":
    main()
