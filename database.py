
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, Session

from settings import DATABASE_URL

Base = declarative_base()

database_url = DATABASE_URL
engine = create_engine(database_url, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("Database URL: ", database_url)
db = None

def get_db():
    global db
    if db is None:
        db = SessionLocal()
    else:
        db = SessionLocal()
    return db


def load_db():
    Base.metadata.create_all(bind=engine)