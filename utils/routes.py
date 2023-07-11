from fastapi import APIRouter

from public.upload_repo import router as upload_router
from public.repos import router as repos_router
from public.chat.api import router as apis_router
from auth.endpoints import auth_router
from users.endpoints import users_router
from public.badges import badges_router
from public.projects import projects_router

routes = APIRouter()
routes.include_router(upload_router)
routes.include_router(repos_router)
routes.include_router(apis_router)
routes.include_router(auth_router)
routes.include_router(users_router)
routes.include_router(badges_router)
routes.include_router(projects_router)
