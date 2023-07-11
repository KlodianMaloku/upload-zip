from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)
    is_supervisor = Column(Boolean, default=False)
    created = Column(DateTime)
    updated = Column(DateTime)

    projects = relationship("Project", back_populates="user")