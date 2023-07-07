from fastapi import Depends, HTTPException, APIRouter
from app.core.model import UserDTO, TweetDTO
from app.core import services
from app.database.database import get_user_repository, get_tweet_repository
from app.database.repositories import RepositoryInterface

router = APIRouter()


@router.post("/users", response_model=UserDTO)
def create_user(
    username: str,
    email: str,
    user_repository: RepositoryInterface = Depends(get_user_repository)
):
    return services.create_user(
        user_repo=user_repository,
        username=username,
        email=email
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


@router.post("/users/{username}/tweets", response_model=TweetDTO)
def create_tweet(
    user_id: int,
    content: str,
    user_repository: RepositoryInterface = Depends(get_user_repository),
    tweet_repository: RepositoryInterface = Depends(get_tweet_repository),
):
    try:
        return services.create_tweet(
            tweet_repo=tweet_repository,
            user_repo=user_repository,
            user_id=user_id,
            content=content,
        )
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
