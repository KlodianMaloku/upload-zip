import datetime

from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str
    badge_id: str
    debt: int
    language: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: str
    description: str
    debt: int
    language: str

class Project(ProjectBase):
    class Config:
        orm_mode = True