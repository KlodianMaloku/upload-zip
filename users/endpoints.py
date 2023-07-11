import string
from datetime import datetime
import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from auth.authentication import get_password_hash
from users.models import User
from users.schemas import UserCreate


users_router = APIRouter()

def gen_uid(prefix):
    return prefix + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

@users_router.post("/register")
def register_user(user: UserCreate):
    db = get_db()
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Create a new user instance
    new_user = User(
        uid=gen_uid('US'),
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        active=True,
        created=datetime.now(),
        updated=datetime.now()
    )

    # Add the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@users_router.get("/users/activate/{uid}")
def activate_user(uid: str):
    db = get_db()
    # Check if the user exists
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Activate the user
    user.active = True
    user.updated = datetime.now()
    db.commit()

    return {"message": "User activated successfully"}

@users_router.get("/users/deactivate/{uid}")
def deactivate_user(uid: str):
    db = get_db()
    # Check if the user exists
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Deactivate the user
    user.active = False
    user.updated = datetime.now()
    db.commit()

    return {"message": "User deactivated successfully"}

@users_router.get("/users/{uid}")
def get_user(uid: str):
    db = get_db()
    # Check if the user exists
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@users_router.get("/users")
def get_users():
    db = get_db()
    return db.query(User).all()
