import re
from dataclasses import dataclass
import datetime

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class EmailAddressError(ValueError):
    ...


class EmailAddress:
    def __init__(self, address):
        self._validate(address)
        self.address = address

    def _validate(self, address):
        if not re.fullmatch(regex, address):
            raise EmailAddressError(f"email: {address} is invalid")

    def __eq__(self, other):
        if isinstance(other, EmailAddress):
            return self.address == other.address
        return False


class User:
    def __init__(
        self,
        user_id: int,
        name: str,
        email: EmailAddress,
        following_relationships: list['FollowerRelationship'] = [],
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.following_relationships = following_relationships

    def add_follow(self, user: 'User'):
        self.following_relationships.append(FollowerRelationship(self, user))


@dataclass
class FollowerRelationship:
    follower: User
    following: User


@dataclass
class Tweet:
    tweet_id: int
    content: str
    user: User
    created_at: datetime.datetime


@dataclass
class TweetDTO:
    tweet_id: int
    content: str
    user_name: str
    created_at: datetime.datetime


class Feed:
    def __init__(self, user: User) -> None:
        self.user = user
        self.tweets: list[TweetDTO] = []

    def add_tweet(self, tweet: Tweet) -> None:
        self.tweets.append(TweetDTO(
            tweet_id=tweet.tweet_id,
            content=tweet.content,
            user_name=tweet.user.name,
            created_at=tweet.created_at,
        ))

    def get_tweets(self) -> list[TweetDTO]:
        return self.tweets


def get_user_feed(user: User, tweets: list[Tweet]) -> Feed:
    feed = Feed(user=user)
    users_to_feed = [user.user_id]
    users_to_feed += [
        rel.following.user_id
        for rel in user.following_relationships
    ]
    for tweet in tweets:
        if tweet.user.user_id in users_to_feed:
            feed.add_tweet(tweet=tweet)
    return feed
