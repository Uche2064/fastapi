from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

# establishing the connection to the db
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# talking to the database requires the sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: creates a session to our databse and closes it after. One session is opened for each query made to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()