from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

"""
models.Model for projects
it will contain the following:
    - uid (primary key) using gen_uid
    - user_id (foreign key) using User.uid
    - name (string)
    - description (string)
    - created (datetime)
    - updated (datetime)
    - badge (one-to-many relationship with Badge)
    - debt (integer)
    - language (string)
    
"""

class Project(Base):
    __tablename__ = "projects"
    uid = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.uid"))
    name = Column(String)
    description = Column(String)
    created = Column(DateTime)
    updated = Column(DateTime)
    badge_id = Column(String, ForeignKey("badges.uid"))
    debt = Column(Integer)
    indexing_done = Column(Integer)
    analysing_done = Column(Integer)
    language = Column(String)

    user = relationship("User", back_populates="projects" )
    badge = relationship("Badge", back_populates="projects")

    def __repr__(self):
        return f"<Project {self.name}>"