from sqlalchemy.orm import Session, contains_eager

import models
import schemas


async def get_user(db: Session, search_param: str):
    return (
        db.query(models.User)
        .join(models.User.address)
        .join(models.User.company)
        .join(models.Address.geo)
        .options(
            contains_eager(models.User.address).contains_eager(models.Address.geo),
            contains_eager(models.User.company),
        )
        .filter(
            (models.User.id == search_param)
            | (models.User.email == search_param)
            | (models.User.username == search_param)
        )
        .first()
    )


async def create_user(db: Session, user: schemas.UserCreate):
    address = models.Address(
        street=user.address.street,
        suite=user.address.suite,
        city=user.address.city,
        zipcode=user.address.zipcode,
        geo=models.Geo(lat=user.address.geo.lat, lng=user.address.geo.lng),
    )
    company = models.Company(
        name=user.company.name, catchphrase=user.company.catchphrase, bs=user.company.bs
    )
    new_user = models.User(
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        website=user.website,
        address=address,
        company=company,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(db: Session, user: models.User, updated_user: schemas.UserUpdate):
    if updated_user.name:
        user.name = updated_user.name

    if updated_user.phone:
        user.phone = updated_user.phone

    if updated_user.website:
        user.website = updated_user.website

    db.commit()
    db.refresh(user)
    return user


async def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    db.close()


async def get_all_users(db: Session):
    return (
        db.query(models.User)
        .join(models.User.address)
        .join(models.User.company)
        .join(models.Address.geo)
        .options(
            contains_eager(models.User.address).contains_eager(models.Address.geo),
            contains_eager(models.User.company),
        )
        .all()
    )
