from fastapi import APIRouter, Depends
from starlette.requests import Request
from fastapi import HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from models.projects import Project as ProjectModel

from database import get_db

router = APIRouter()

@router.get("/get-projects")
async def list_repos(request: Request):
    db = get_db()
    repos = []
    projects = db.query(ProjectModel).filter(ProjectModel.user_id == request.state.user.uid)
    if not projects:
        raise HTTPException(status_code=404, detail='Project not found')

    for project in projects:
        pr = {
            "uid": project.uid,
            "name": project.name,
            "description": project.description,
            "created": str(project.created),
            "created_by": project.user.username,
            "badge": project.badge.name,
            "debt": project.debt,
            "language": project.language,
        }
        repos.append(pr)

    return  JSONResponse(content=repos, status_code=200)