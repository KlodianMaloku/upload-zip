import shutil
from datetime import datetime

from fastapi import HTTPException, APIRouter
from sqlalchemy import func
from starlette.requests import Request
from sqlalchemy.exc import IntegrityError

from database import get_db
from integrations.qdrant.qdrant_core import QdrantCore
from models.badges import Badge as BadgeModel
from models.projects import Project as ProjectModel
from models.schemas.projects import ProjectCreate, ProjectUpdate, Project
from users.endpoints import gen_uid

projects_router = APIRouter()


@projects_router.post('/projects/', response_model=Project)
def create_project(project_data: ProjectCreate, request: Request):

    db = get_db()

    badge = db.query(BadgeModel).order_by(func.random()).first()

    try:
        project = ProjectModel(
            uid=gen_uid('PR'),
            name=project_data.name.replace(' ', '-'),
            description=project_data.description,
            created=datetime.now(),
            badge_id=badge.uid if badge else None,
            debt=project_data.debt,
            indexing_done=1,
            analysing_done=1,
            language=project_data.language,
            user_id=request.state.user.uid
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Project creation failed')


@projects_router.get('/projects/{project_uid}', response_model=Project)
def get_project(project_uid: str, request: Request):
    db = get_db()
    project = db.query(ProjectModel).filter(ProjectModel.uid == project_uid,
                                            ProjectModel.user_id == request.state.user.uid
                                            ).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    return project


@projects_router.put('/projects/{project_uid}', response_model=Project)
def update_project(project_uid: str, project_data: ProjectUpdate, request: Request):
    db = get_db()
    project = db.query(ProjectModel).filter(ProjectModel.uid == project_uid).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    for field, value in project_data.dict().items():
        if field == 'updated':
            value = datetime.now()
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@projects_router.delete('/projects/{project_uid}')
def delete_project(project_uid: str, request: Request):
    """
    Delete project by UID
        1. Delete project folder at projects folder where the project_name is the folder name
        2. Delete index with project name from qudrant
        3. Delete project from database
    """
    db = get_db()
    project = db.query(ProjectModel).filter(ProjectModel.uid == project_uid).first()

    project_dir = f'projects/{project.name}'
    shutil.rmtree(project_dir)

    client = QdrantCore().client
    client.delete_collection(project.name)


    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    db.delete(project)
    db.commit()
    return {'message': 'Project deleted successfully'}