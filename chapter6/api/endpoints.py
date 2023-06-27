from fastapi import Depends, HTTPException, APIRouter
from core.model import User, TweetDTO, Tweet
from database.schema import mapper_registry
from database import get_user_repository, get_tweet_repository
from database.repositories import UserRepository, TweetRepository

mapper_registry.metadata.create_all()

router = APIRouter()


def get_user_by_username(
    user_repository: UserRepository,
    username: str,
) -> User:
    user = user_repository.get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{username}", response_model=User)
def get_user(
    username: str,
    user_repository: UserRepository = Depends(get_user_repository)
):
    user = get_user_by_username(user_repository, username)
    return user


@router.post("/users/{username}/tweets", response_model=TweetDTO)
def create_tweet(
    username: str,
    content: str,
    user_repository: UserRepository = Depends(get_user_repository),
    tweet_repository: TweetRepository = Depends(get_tweet_repository),
):
    user = get_user_by_username(user_repository, username)
    tweet = Tweet(user=user, content=content)
    user.post_tweet(tweet)
    tweet_repository.add(tweet)
    return TweetDTO(
        tweet_id=tweet.id,
        username=user.username,
        content=tweet.content,
        timestamp=tweet.timestamp,
        num_likes=len(tweet.likes)
    )


@router.get("/users/{username}/feed", response_model=list[TweetDTO])
def get_feed(
    username: str,
    user_repository: UserRepository = Depends(get_user_repository)
):
    user = get_user_by_username(user_repository, username)
    feed = user.get_feed()
    return feed
