from datetime import timedelta

from fastapi import HTTPException, APIRouter
from auth.authentication import verify_password

from database import get_db
from auth.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from users.models import User
auth_router = APIRouter()

@auth_router.post("/login")
def login_user(username: str, password: str):
    # Check if the user exists
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.uid, "email": user.email}, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}