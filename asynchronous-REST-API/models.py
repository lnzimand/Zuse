from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Geo(Base):
    __tablename__ = "geo"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String)
    lng = Column(String)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    suite = Column(String)
    city = Column(String)
    zipcode = Column(String)
    geo_id = Column(Integer, ForeignKey("geo.id"))

    geo = relationship("Geo", backref="address")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    catchphrase = Column(String)
    bs = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    website = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"))
    company_id = Column(Integer, ForeignKey("company.id"))

    address = relationship("Address", backref="users")
    company = relationship("Company", backref="users")
