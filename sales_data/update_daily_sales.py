# -------------------- update_daily_sales.py --------------------
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sp_api.api import Sales
from sp_api.base import Granularity, Marketplaces
from sp_api.auth.exceptions import AuthorizationError
from db.connect import SessionLocal
from db.models import SalesSummary
from client_config import CREDENTIALS
from logger import logger

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

marketplace_credentials = {
    mp: CREDENTIALS[region] for mp, region in [
        (Marketplaces.US, "North America"),
        (Marketplaces.CA, "North America"),
        (Marketplaces.MX, "North America"),
        (Marketplaces.DE, "Europe"),
        (Marketplaces.FR, "Europe"),
        (Marketplaces.IT, "Europe"),
        (Marketplaces.ES, "Europe"),
        (Marketplaces.NL, "Europe"),
        (Marketplaces.BE, "Europe"),
        (Marketplaces.SE, "Europe"),
        (Marketplaces.PL, "Europe"),
        (Marketplaces.TR, "Europe"),
        (Marketplaces.UK, "Europe"),
        (Marketplaces.JP, "Far East"),
        (Marketplaces.AU, "Australia")
    ]
}

def fetch_and_store():
    session = SessionLocal()
    for mp, tz in marketplace_timezones.items():
        try:
            local_tz = pytz.timezone(tz)
            end_dt = datetime.now(local_tz).replace(hour=23, minute=59)
            start_dt = end_dt - timedelta(days=3)
            start_str = start_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_str = end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

            logger.info(f"Fetching {mp.name} sales between {start_str} and {end_str}")
            res = Sales(credentials=marketplace_credentials[mp], marketplace=mp)
            data = res.get_order_metrics(
                granularity=Granularity.DAY,
                interval=(start_str, end_str),
                granularityTimeZone=tz
            )

            for entry in data.payload:
                date_str = entry['interval'].split('T')[0]
                existing = session.query(SalesSummary).filter_by(date=date_str, country=mp.name).first()
                if existing:
                    logger.info(f"Skipping duplicate record for {mp.name} on {date_str}")
                    continue

                summary = SalesSummary(
                    date=date_str,
                    country=mp.name,
                    average_unit_price=entry['averageUnitPrice']['amount'],
                    order_item_count=entry['orderItemCount'],
                    unit_count=entry['unitCount'],
                    total_sales=entry['totalSales']['amount'],
                    currency=entry['totalSales']['currencyCode']
                )
                session.add(summary)
                session.commit()
                logger.info(f"Inserted summary for {mp.name} on {date_str}")

        except AuthorizationError as e:
            logger.error(f"Auth error for {mp.name}: {e}")
        except Exception as e:
            logger.error(f"Error fetching sales for {mp.name}: {e}")

    session.close()

if __name__ == "__main__":
    fetch_and_store()