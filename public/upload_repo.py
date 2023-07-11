from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request

from models.badges import Badge
from models.projects import Project
from models.schemas.projects import ProjectCreate
from shikimi.core.index import *
from users.endpoints import gen_uid
from database import SessionLocal, get_db

router = APIRouter()

@router.post("/upload-zip")
async def upload_zip(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Create a temporary directory to extract the contents of the ZIP file
    project_name = file.filename.split('.')[0].replace(' ', '-')
    temp_dir = f'./temp_{project_name}'
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, project_name + '.zip')

    try:
        # Save the uploaded ZIP file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        root_path = os.path.dirname(os.path.abspath(__file__)).strip('public')
        # Extract the contents of the ZIP file to a specific folder
        extract_dir = os.path.join(root_path, 'projects', project_name)
        os.makedirs(extract_dir, exist_ok=True)
        shutil.unpack_archive(file_path, extract_dir)
        # Remove the __MACOSX directory if it exists
        macosx_dir = os.path.join(extract_dir, '__MACOSX')
        if os.path.exists(macosx_dir):
            shutil.rmtree(macosx_dir)

        # save project to database
        badge = db.query(Badge).order_by(func.random()).first()
        project_data = ProjectCreate(name=project_name, description=project_name,
                                     debt=0, language='python', badge_id=badge.uid if badge else None)
        try:
            project = Project(
                uid=gen_uid('PR'),
                name=project_name,
                description=project_name,
                created=datetime.now(),
                badge_id=badge.uid if badge else None,
                debt=project_data.debt,
                language=project_data.language,
                user_id=request.state.user.uid
            )
            db.add(project)
            db.commit()
            db.refresh(project)
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Project creation failed')

        return {"message": "ZIP file uploaded and extracted successfully"}
    finally:
        # Clean up - remove the temporary directory and file
        shutil.rmtree(temp_dir)


@router.get("/analyze-directory/{dirname}")
async def analyze_directory(dirname: str):
    base_path = os.path.dirname(os.path.abspath(__file__)).strip('public')
    directory_path = os.path.join(base_path, 'projects', dirname)

    # Check if the directory exists
    if not os.path.exists(directory_path):
        raise HTTPException(status_code=404, detail="Directory not found")

    # Function to traverse the directory and build the structure
    def traverse_directory(path):
        dir_dict = {"type": "directory", "name": os.path.basename(path), "children": []}

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if os.path.isdir(item_path):
                dir_dict["children"].append(traverse_directory(item_path))
            else:
                dir_dict["children"].append({"type": "file", "name": item})

        return dir_dict

    # Traverse the directory and build the structure
    structure = traverse_directory(directory_path)
    return structure
