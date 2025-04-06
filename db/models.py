from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

# ──────────────────────────────
# 1. Top-level Amazon Orders
# ──────────────────────────────
class AmazonOrder(Base):
    __tablename__ = 'amazon_orders'

    id = Column(Integer, primary_key=True, index=True)
    amazon_order_id = Column(String, unique=True, nullable=False)
    purchase_date = Column(DateTime)
    buyer_email = Column(String)

# ──────────────────────────────
# 2. Daily Sales Summary
# ──────────────────────────────
class SalesSummary(Base):
    __tablename__ = "sales_summary"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    country = Column(String, nullable=False)
    average_unit_price = Column(String)
    order_item_count = Column(Integer)
    unit_count = Column(Integer)
    total_sales = Column(String)
    currency = Column(String)

# ──────────────────────────────
# 3. Order Detail Header Table
# ──────────────────────────────
class AmazonOrderDetail(Base):
    __tablename__ = "amazon_orders_detail"

    id = Column(Integer, primary_key=True, index=True)
    amazon_order_id = Column(String, unique=True, nullable=False)  # ✅ UNIQUE for FK
    purchase_date = Column(DateTime)
    order_status = Column(String)
    buyer_name = Column(String)
    buyer_email = Column(String)
    marketplace_id = Column(String)
    order_total = Column(String)
    currency = Column(String)

    items = relationship(
        "AmazonOrderDetailItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

# ──────────────────────────────
# 4. Order Detail Item Table
# ──────────────────────────────
class AmazonOrderDetailItem(Base):
    __tablename__ = "amazon_order_detail_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("amazon_orders_detail.amazon_order_id"), nullable=False)

    asin = Column(String)
    seller_sku = Column(String)
    title = Column(String)
    quantity_ordered = Column(Integer)
    item_price = Column(Float)
    item_currency = Column(String)
    shipping_price = Column(Float)
    shipping_currency = Column(String)
    country = Column(String)
    unit_price = Column(Float)

    order = relationship("AmazonOrderDetail", back_populates="items")
