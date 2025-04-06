import sys
import os
import logging
from datetime import datetime, timedelta, timezone
import pandas as pd
from sqlalchemy.exc import IntegrityError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client_config import CREDENTIALS as credentials
from sp_api.api import Sales
from sp_api.base import Granularity, Marketplaces
from sp_api.auth.exceptions import AuthorizationError
from db.connect import SessionLocal
from db.models import SalesSummary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch and format sales data
def fetch_sales_data(start_date, end_date, country, credentials):
    res = Sales(credentials=credentials, marketplace=country)
    try:
        data = res.get_order_metrics(granularity=Granularity.DAY, interval=(start_date, end_date))
    except AuthorizationError as e:
        logger.error(f"Authorization error for {country.name}: {e}")
        return []

    rows = []
    if data.payload:
        for entry in data.payload:
            row = {
                'Date': entry['interval'].split('T')[0],
                'Average Unit Price': entry['averageUnitPrice']['amount'],
                'Order Item Count': entry['orderItemCount'],
                'Unit Count': entry['unitCount'],
                'Total Sales': entry['totalSales']['amount'],
                'Currency': entry['totalSales']['currencyCode'],
                'Country': country.name
            }
            rows.append(row)

    return rows

# DB session
session = SessionLocal()

# Define start and end dates
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=720)

start_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
end_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

# Define a mapping of marketplaces to their corresponding credentials
marketplace_credentials = {
    Marketplaces.US: credentials["North America"],
    Marketplaces.CA: credentials["North America"],
    Marketplaces.MX: credentials["North America"],
    Marketplaces.DE: credentials["Europe"],
    Marketplaces.FR: credentials["Europe"],
    Marketplaces.IT: credentials["Europe"],
    Marketplaces.ES: credentials["Europe"],
    Marketplaces.NL: credentials["Europe"],
    Marketplaces.BE: credentials["Europe"],
    Marketplaces.SE: credentials["Europe"],
    Marketplaces.PL: credentials["Europe"],
    Marketplaces.TR: credentials["Europe"],
    Marketplaces.UK: credentials["Europe"],
    Marketplaces.JP: credentials["Far East"],
    Marketplaces.AU: credentials["Australia"]
}

# List of marketplaces to fetch data for
marketplaces = list(marketplace_credentials.keys())

# Fetch data and store in DB and Excel
all_data = []
inserted = 0
skipped = 0

for marketplace in marketplaces:
    logger.info(f"Fetching data for {marketplace.name}...")
    country_data = fetch_sales_data(start_str, end_str, marketplace, marketplace_credentials[marketplace])
    for row in country_data:
        try:
            obj = SalesSummary(
                date=datetime.strptime(row['Date'], '%Y-%m-%d'),
                average_unit_price=row['Average Unit Price'],
                order_item_count=row['Order Item Count'],
                unit_count=row['Unit Count'],
                total_sales=row['Total Sales'],
                currency=row['Currency'],
                country=row['Country']
            )
            session.add(obj)
            session.commit()
            inserted += 1
        except IntegrityError:
            session.rollback()
            skipped += 1
    all_data.extend(country_data)

logger.info(f"Inserted: {inserted}, Skipped (duplicates or errors): {skipped}")

# Save to Excel
df = pd.DataFrame(all_data)
excel_filename = 'sales_data.xlsx'
df.to_excel(excel_filename, index=False)
logger.info(f"Data has been written to {excel_filename}")
