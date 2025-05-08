from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "sqlite:///./test.db"
# db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
db_engine = create_engine(DATABASE_URL)
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
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db_session.close()
