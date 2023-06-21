from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from helpers import process_users

import models
import schemas
import services

from database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/users/{user_id}", response_model=schemas.UserDetails)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await services.get_user(db=db, search_param=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api/v1/users", response_model=schemas.UserDetails)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    email_exists = await services.get_user(db=db, search_param=user.email)
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    username_exists = await services.get_user(db=db, search_param=user.username)
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    return await services.create_user(db=db, user=user)


@app.put("/api/v1/users/{user_id}")
async def update_user(
    user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = await services.get_user(db=db, search_param=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await services.update_user(db=db, user=user, updated_user=updated_user)
    return {"message": "User updated successfully"}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await services.delete_user(db=db, user=user)
    return {"message": "User deleted successfully"}


@app.get("/api/v1/users", response_model=List[schemas.UserDetails])
async def get_all_users(db: Session = Depends(get_db)):
    return services.get_all_users(db=db)


@app.on_event("startup")
async def prepare_users():
    db = SessionLocal()
    process_users(db)
