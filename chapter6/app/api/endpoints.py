from dataclasses import dataclass

from fastapi import APIRouter, Depends, HTTPException

from app.core import services
from app.core.model import TweetDTO, UserDTO
from app.database.database import get_tweet_repository, get_user_repository
from app.database.repositories import RepositoryInterface

router = APIRouter()


@dataclass
class UserInput:
    username: str
    email: str


@dataclass
class TweetInput:
    user_id: int
    content: str


@router.post("/users", response_model=UserDTO)
def create_user(
    user: UserInput,
    user_repository: RepositoryInterface = Depends(get_user_repository)
):
    return services.create_user(
        user_repo=user_repository,
        username=user.username,
        email=user.email
    )


@router.get("/users/{user_id}", response_model=UserDTO)
def get_user(
    user_id: int,
    user_repository: RepositoryInterface = Depends(get_user_repository)
):
    try:
        return services.get_user_by_id(
            user_repo=user_repository,
            user_id=user_id,
        )
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tweets", response_model=TweetDTO)
def create_tweet(
    tweet: TweetInput,
    user_repository: RepositoryInterface = Depends(get_user_repository),
    tweet_repository: RepositoryInterface = Depends(get_tweet_repository),
):
    try:
        return services.create_tweet(
            tweet_repo=tweet_repository,
            user_repo=user_repository,
            user_id=tweet.user_id,
            content=tweet.content,
        )
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
