from typing import List
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from helpers import process_users, user_to_dict

import schemas
import services
import html

from database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def process_user_action(db: Session, action: str, data: dict):
    if action == "get_user":
        user_id = data.get("user_id")
        user = await services.get_user(db=db, search_param=user_id)
        if not user:
            return {"message": "User not found"}
        return {"message": "User found", "user": user_to_dict(user)}

    elif action == "delete_user":
        user_id = data.get("user_id")
        user = await services.get_user(db=db, search_param=user_id)
        if not user:
            return {"message": "User not found"}
        await services.delete_user(db=db, user=user)
        return {"message": "User deleted successfully"}

    elif action == "update_user":
        user_id = data.get("user_id")
        updated_user = data.get("updated_user")
        user = await services.get_user(db=db, search_param=user_id)
        if not user:
            return {"message": "User not found"}
        await services.update_user(
            db=db, user=user, updated_user=schemas.UserUpdate(**updated_user)
        )
        return {"message": "User updated successfully"}

    elif action == "get_all_users":
        users = await services.get_all_users(db=db)
        user_dicts = [user_to_dict(user) for user in users]
        return {"message": f"{len(users)} users found", "users": user_dicts}

    else:
        return {"message": "Invalid action"}


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
    user = services.get_user(db=db, search_param=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await services.delete_user(db=db, user=user)
    return {"message": "User deleted successfully"}


@app.get("/api/v1/users", response_model=List[schemas.UserDetails])
async def get_all_users(db: Session = Depends(get_db)):
    return await services.get_all_users(db=db)


@app.get("/")
async def home():
    return HTMLResponse(html.html)


@app.websocket("/ws-basic")
async def basic_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


@app.websocket("/ws-advanced")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        action = data.get("action")
        result = await process_user_action(db=db, action=action, data=data)
        await websocket.send_json(result)


@app.on_event("startup")
async def prepare_users():
    db = SessionLocal()
    process_users(db)
