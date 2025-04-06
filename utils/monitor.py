import sys
import os
import logging
from sqlalchemy.sql import func
from sqlalchemy import and_, distinct

# Dynamically add the root project dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connect import SessionLocal
from db.models import SalesSummary, AmazonOrderDetail, AmazonOrderDetailItem

# Setup session
session = SessionLocal()

print("\n--- ✅ Recent SalesSummary Records ---")
sales_check = session.query(SalesSummary.date, SalesSummary.country).order_by(SalesSummary.date.desc()).limit(10).all()
for r in sales_check:
    print(r)

# ------------------ 🔍 Integrity Checks -------------------
print("\n--- 🧪 Data Integrity Audit ---")

# 1. Null check: unit_count in SalesSummary
null_units = session.query(SalesSummary).filter(SalesSummary.unit_count == None).count()
print(f"Null unit_count rows in SalesSummary: {null_units}")

# 2. Null check: order_id in AmazonOrderDetail
null_orders = session.query(AmazonOrderDetail).filter(AmazonOrderDetail.amazon_order_id == None).count()
print(f"Null amazon_order_id in AmazonOrderDetail: {null_orders}")

# 3. Check duplicates for date + country in SalesSummary
duplicates = (
    session.query(SalesSummary.date, SalesSummary.country, func.count('*').label("count"))
    .group_by(SalesSummary.date, SalesSummary.country)
    .having(func.count('*') > 1)
    .all()
)
print(f"Duplicate SalesSummary date+country records: {len(duplicates)}")
if duplicates:
    print("Sample Duplicates:")
    for row in duplicates[:5]:
        print(row)

# 4. Currency consistency check
print("\nCurrency mismatches (per country):")
currency_issues = (
    session.query(SalesSummary.country, SalesSummary.currency, func.count('*'))
    .group_by(SalesSummary.country, SalesSummary.currency)
    .having(func.count('*') > 1)
    .all()
)
if currency_issues:
    for issue in currency_issues:
        print(issue)
else:
    print("✅ All currencies consistent")

# 5. Orders missing line items
missing_items = (
    session.query(AmazonOrderDetail.amazon_order_id)
    .outerjoin(AmazonOrderDetailItem, AmazonOrderDetail.amazon_order_id == AmazonOrderDetailItem.order_id)
    .filter(AmazonOrderDetailItem.id == None)
    .all()
)
print(f"Orders with no item detail: {len(missing_items)}")

# Cleanup
session.close()
print("\n--- 🟢 Monitor Checks Complete ---")