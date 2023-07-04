from fastapi import Depends, HTTPException, APIRouter
from app.core.model import UserDTO, TweetDTO
from app.core import services
from app.database.database import get_user_repository, get_tweet_repository
from app.database.repositories import UserRepository, TweetRepository

router = APIRouter()


@router.post("/users", response_model=UserDTO)
def create_user(
    username: str,
    email: str,
    user_repository: UserRepository = Depends(get_user_repository)
):
    return services.create_user(
        user_repo=user_repository,
        username=username,
        email=email
    )


@router.get("/users/{username}", response_model=UserDTO)
def get_user(
    username: str,
    user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        return services.get_user_by_username(
            user_repo=user_repository,
            username=username,
        )
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users/{username}/tweets", response_model=TweetDTO)
def create_tweet(
    username: str,
    content: str,
    user_repository: UserRepository = Depends(get_user_repository),
    tweet_repository: TweetRepository = Depends(get_tweet_repository),
):
    try:
        return services.create_tweet(
            tweet_repo=tweet_repository,
            user_repo=user_repository,
            username=username,
            content=content,
        )
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
