from fastapi import HTTPException
import requests
from sqlalchemy.orm import Session
from models import Address, Company, Geo, User


def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Failed to fetch users from the external API."
        )
    return response.json()


def process_users(db: Session):
    users_data = fetch_users()
    try:
        for user_data in users_data:
            address_data = user_data["address"]
            geo_data = address_data.pop("geo")

            geo = Geo(**geo_data)
            address = Address(geo=geo, **address_data)
            company = Company(
                name=user_data["company"]["name"],
                catchphrase=user_data["company"]["catchPhrase"],
                bs=user_data["company"]["bs"],
            )

            user = User(
                id=user_data["id"],
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
                phone=user_data["phone"],
                website=user_data["website"],
                address=address,
                company=company,
            )

            db.merge(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to process users data."
        ) from e


def user_to_dict(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "website": user.website,
    }


class DotDict(dict):
    def __getattr__(self, attr):
        value = self[attr]
        if isinstance(value, dict):
            value = DotDict(value)
        return self[attr]

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, dict):
            value = DotDict(value)
        return value
