from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from databases import Database
from dotenv import load_dotenv
import os

from database.repositories import UserRepository, TweetRepository

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def connect_to_database():
    database = Database(DATABASE_URL)
    await database.connect()
    return database


async def close_database_connection(database: Database):
    await database.disconnect()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_tweet_repository(db: Session = Depends(get_db)) -> TweetRepository:
    return TweetRepository(db)
