from db.connect import engine
from db.models import Base, AmazonOrder, SalesSummary, AmazonOrderDetail
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
