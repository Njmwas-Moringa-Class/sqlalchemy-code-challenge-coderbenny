#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Restaurant, Review, restaurant_customers

faker = Faker()

def add_customer_to_join(session):
        for review in session.query(Review):
            existing = session.query(restaurant_customers).filter_by(customer_id=review.customer_id, restaurant_id=review.restaurant_id).first()
            if not existing:
                session.execute(restaurant_customers.insert().values(customer_id=review.customer_id, restaurant_id=review.restaurant_id))
                session.commit()


if __name__ == '__main__':
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    add_customer_to_join(session)
    print("Customers who have made reviews have been added!")

