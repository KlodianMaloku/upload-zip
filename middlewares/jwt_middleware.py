from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth.authentication import decode_access_token
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from database import SessionLocal
from users.models import User


class JwtAuthentication(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next ):
        unprotected_routes = ['/api/register', '/api/docs', '/api/openapi.json', '/api/login']
        db: Session = SessionLocal()
        if not request.url.path in unprotected_routes:
            try:
                uid = decode_access_token(request.headers['Authorization'].split(' ')[1])
                user = db.query(User).filter(User.uid == uid).first()
            except HTTPException as e:
                return JSONResponse(status_code=401, content="Invalid token")

            if not user:
                return JSONResponse(status_code=404, content="User not found")

            if not user.active:
                return JSONResponse(status_code=401, content="User is not active")

            request.state.user = user

        response = await call_next(request)
        return response