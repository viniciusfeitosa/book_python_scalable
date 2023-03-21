import pytest
from datetime import datetime

from domain import (
    EmailAddress,
    EmailAddressError,
    FollowerRelationship,
    Tweet,
    User,
    get_user_feed,
)


def test_user_creation():
    user = User(
        user_id=1,
        name="John Doe",
        email=EmailAddress("john.doe@example.com"),
    )
    assert user.user_id == 1
    assert user.name == "John Doe"
    assert user.email == EmailAddress("john.doe@example.com")


def test_tweet_creation():
    user = User(
        user_id=1,
        name="John Doe",
        email=EmailAddress("john.doe@example.com"),
    )
    tweet = Tweet(
        tweet_id=1,
        content="Hello, world!",
        user=user,
        created_at=datetime.utcnow(),
    )
    assert tweet.tweet_id == 1
    assert tweet.content == "Hello, world!"
    assert tweet.user == user


def test_email_address_validation():
    with pytest.raises(EmailAddressError):
        EmailAddress("invalid-email")


def test_email_address_equality():
    email1 = EmailAddress("john.doe@example.com")
    email2 = EmailAddress("john.doe@example.com")
    email3 = EmailAddress("jane.doe@example.com")
    assert email1 == email2
    assert email1 != email3


def test_create_follower_relationship():
    user1 = User(
        user_id=1,
        name="John Doe",
        email=EmailAddress("john.doe@example.com"),
    )
    user2 = User(
        user_id=1,
        name="Jane Doe",
        email=EmailAddress("jane.doe@example.com"),
    )
    relationship = FollowerRelationship(follower=user1, following=user2)
    assert relationship.follower == user1
    assert relationship.following == user2


def test_read_feed():
    user1 = User(
        user_id=1,
        name="John Doe",
        email=EmailAddress("john.doe@example.com"),
    )
    user2 = User(
        user_id=1,
        name="Jane Doe",
        email=EmailAddress("jane.doe@example.com"),
    )
    user3 = User(
        user_id=3,
        name="Non Used",
        email=EmailAddress("non.used@example.com"),
    )
    user1.add_follow(user2)

    tweets = [
        Tweet(
            tweet_id=1,
            content="Hello World",
            user=user1,
            created_at=datetime.utcnow(),
        ),
        Tweet(
            tweet_id=2,
            content="Hola que tal",
            user=user2,
            created_at=datetime.utcnow(),
        ),
        Tweet(
            tweet_id=3,
            content="Hey hey!",
            user=user2,
            created_at=datetime.utcnow(),
        ),
        Tweet(
            tweet_id=4,
            content="Non used tweet",
            user=user3,
            created_at=datetime.utcnow(),
        )
    ]

    feed = get_user_feed(user=user1, tweets=tweets)
    assert len(feed.tweets) == 3
    assert feed.get_tweets()[2].tweet_id == 3
    assert feed.get_tweets()[2].user_name == 'Jane Doe'
