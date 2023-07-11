from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

"""
models.Model for badges
it will contain the following:
    - uid (primary key) using gen_uid
    - name (string)
    - description (string)
    
    uid will be a foreign key in the projects model
    
"""

class Badge(Base):
    __tablename__ = "badges"
    uid = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    projects = relationship("Project", back_populates="badge")

    def __repr__(self):
        return f"<Badge {self.name}>"