from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# import os

# DATABASE_URL = os.getenv("DATABASE_URL")// PostgreSQL
# db_engine = create_engine(DATABASE_URL)// PostgreSQL
DATABASE_URL = "sqlite:///./indoor_system.db"
db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DBSession = sessionmaker(
    bind=db_engine, 
    autocommit=False, 
    autoflush=False
)
ORMBaseModel = declarative_base()

def get_db_session():
    db_session = DBSession()
    try:
        yield db_session
    finally:
        db_session.close()
