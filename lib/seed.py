#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Review

faker = Faker()

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Review).delete()

    print("Adding reviews...")

    reviews = [
            Review(
                star_rating = random.randint(0,10),
                restaurant_id = random.randint(1,4),
                customer_id = random.randint(1,10)
            )
        for _ in range(20)
    ]

    session.add_all(reviews)
    session.commit()

    print("Reviews added succesfully!")
