import os

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.repositories import TweetRepository, UserRepository

DATABASE_URL = os.getenv("DB_URL", "")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_tweet_repository(db: Session = Depends(get_db)) -> TweetRepository:
    return TweetRepository(db)
