from pydantic import BaseModel

class BadgeBase(BaseModel):
    name: str
    description: str

class BadgeCreate(BadgeBase):
    pass

class BadgeUpdate(BadgeBase):
    pass

class Badge(BadgeBase):
    class Config:
        orm_mode = True