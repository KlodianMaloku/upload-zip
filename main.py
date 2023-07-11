from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from socketio import ASGIApp


from middlewares.jwt_middleware import JwtAuthentication
from middlewares.throttling_middleware import ThrottlingMiddleware
from public.chat.sockets_events import sio
from utils.routes import routes
from database import load_db

app = FastAPI(title="TechDebtGPT sockets", version="1.0.0")

api_app = FastAPI(title="TechDebtGPT API", version="1.0.0")

load_db()

origins = [
    "http://localhost:3000",
    "https://techdebtgpt.ngrok.io",
    "https://app.techdebtgpt.com",
    # Add more origins as needed
]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_app.add_middleware(JwtAuthentication)
api_app.add_middleware(ThrottlingMiddleware)

api_app.include_router(routes)
app.mount("/api", api_app)

def custom_openapi():
    if api_app.openapi_schema:
        return api_app.openapi_schema
    openapi_schema = get_openapi(
        title="TechDebtGPT API",
        version="1.0.0",
        description="Backend API for TechDebtGPT",
        routes=api_app.routes,
    )
    api_app.openapi_schema = openapi_schema
    return api_app.openapi_schema


socket_app = FastAPI()
sio_asgi_app = ASGIApp(socketio_server=sio)
socket_app.mount("/", sio_asgi_app)

app.openapi = custom_openapi

app.mount("/", socket_app)

