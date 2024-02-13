import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey, Table)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
session = sessionmaker(bind=engine)

restaurant_customers = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(),primary_key=True)
    star_rating = Column(Integer())

    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', backref='reviews')
    customer = relationship('Customer', backref='reviews')

    def __repr__(self):
        return f'Review: {self.star_rating}'

    def customer(self):
        return self.customer
    
    def restaurant(self):
        return self.restaurant

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)

    # Table Relationships
    reviews_relationship = relationship('Review', backref='restaurant')
    customers_relationship = relationship('Customer', secondary=restaurant_customers, back_populates='restaurants')


    def __repr__(self):
        return f'Restaurant: {self.name}'

    def reviews(self):
        return self.reviews_relationship

    
    def customers(self):
        return self.customers_relationship


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    # Table Relationships
    reviews_relationship = relationship('Review', backref='customer')
    restaurants_relationship = relationship('Restaurant', secondary=restaurant_customers, back_populates='customers')


    def __repr__(self):
        return f'Customer: {self.first_name} {self.last_name}'
    
    def reviews(self):
        return self.reviews_relationship
    
    def restaurants(self):
        return set([rest.name for rest in self.restaurants_relationship])
