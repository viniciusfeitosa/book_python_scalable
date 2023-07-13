from app.core.model import Tweet, TweetDTO, User, UserDTO
from app.database.repositories import RepositoryPort


class UserNotFoundError(Exception):
    ...


def create_user(
    user_repo: RepositoryPort,
    username: str,
    email: str,
) -> UserDTO:
    user = user_repo.add(User(username=username, email=email))
    return UserDTO(
        user_id=user.id,
        username=user.username,
        email=user.email,
    )


def get_user_by_id(
    user_repo: RepositoryPort,
    user_id: int,
) -> UserDTO:
    user = user_repo.get_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"Not found user_id: {user_id}")
    return UserDTO(
        user_id=user.id,
        username=user.username,
        email=user.email,
    )


def create_tweet(
    tweet_repo: RepositoryPort,
    user_repo: RepositoryPort,
    user_id: int,
    content: str,
) -> TweetDTO:
    user = user_repo.get_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"Not found user_id: {user_id}")
    tweet = tweet_repo.add(Tweet(user=user, content=content))
    return TweetDTO(
        tweet_id=tweet.id,
        username=user.username,
        content=tweet.content,
        timestamp=tweet.timestamp,
        num_likes=len(tweet.likes)
    )
