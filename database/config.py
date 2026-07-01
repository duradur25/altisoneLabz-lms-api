from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
ACCESS_TOKEN_EXPIRED_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES"))
REFRESH_TOKEN_EXPIRED_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRED_DAYS"))
ALGORITHM = os.getenv("ALGORITHM")

engine = create_engine(DATABASE_URL, echo=True)

from sqlalchemy.orm import sessionmaker

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass