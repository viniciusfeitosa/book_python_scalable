from app.database.repositories import UserRepository, TweetRepository
from app.core.model import User, UserDTO, Tweet, TweetDTO


class UserNotFoundError(Exception):
    ...


def create_user(
    user_repo: UserRepository,
    username: str,
    email: str,
) -> UserDTO:
    user = user_repo.add(User(username=username, email=email))
    return UserDTO(
        user_id=user.id,
        username=user.username,
        email=user.email,
    )


def get_user_by_username(
    user_repo: UserRepository,
    username: str,
) -> UserDTO:
    user = user_repo.get_by_username(username)
    if user is None:
        raise UserNotFoundError(f"Not found username: {username}")
    return UserDTO(
        user_id=user.id,
        username=user.username,
        email=user.email,
    )


def create_tweet(
    tweet_repo: TweetRepository,
    user_repo: UserRepository,
    username: str,
    content: str,
) -> TweetDTO:
    user = user_repo.get_by_username(username)
    if user is None:
        raise UserNotFoundError(f"Not found username: {username}")
    tweet = tweet_repo.add(Tweet(user=user, content=content))
    return TweetDTO(
        tweet_id=tweet.id,
        username=user.username,
        content=tweet.content,
        timestamp=tweet.timestamp,
        num_likes=len(tweet.likes)
    )
