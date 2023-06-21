from typing import Optional
from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    username: Optional[str]
    email: Optional[str]


class GeoCreate(BaseModel):
    lat: str
    lng: str


class GeoDetails(BaseModel):
    lat: str
    lng: str

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoCreate


class AddressDetails(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoDetails

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    name: str
    catchphrase: str
    bs: str


class CompanyDetails(BaseModel):
    name: str
    catchphrase: str
    bs: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: AddressCreate
    company: CompanyCreate


class UserDetails(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: AddressDetails
    company: CompanyDetails

    class Config:
        orm_mode = True
