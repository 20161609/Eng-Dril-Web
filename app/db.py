from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

database_url = 'sqlite:///./engdrill.db'
engine = create_engine(database_url, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)