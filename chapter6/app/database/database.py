from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
import os

from app.database.schema import mapper_registry
from app.database.repositories import UserRepository, TweetRepository

DATABASE_URL = os.getenv("DB_URL", "")

engine = create_engine(DATABASE_URL)
mapper_registry.metadata.create_all(engine)

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
