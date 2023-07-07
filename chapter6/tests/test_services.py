import pytest

from app.database import repositories
from app.core import services


def test_service_create_user(session):
    repo = repositories.UserRepository(session)
    dto = services.create_user(
        user_repo=repo,
        username='test',
        email='test@test.com',
    )
    assert dto.user_id == 1
    assert dto.username == 'test'
    assert dto.email == 'test@test.com'


def test_service_get_user_by_id(session):
    repo = repositories.UserRepository(session)
    with pytest.raises(services.UserNotFoundError) as err:
        services.get_user_by_id(
            user_repo=repo,
            user_id=1,
        )
    assert str(err.value) == 'Not found user_id: 1'
    services.create_user(
        user_repo=repo,
        username='test',
        email='test@test.com',
    )
    dto = services.get_user_by_id(
        user_repo=repo,
        user_id=1,
    )
    assert dto.user_id == 1
    assert dto.username == 'test'
    assert dto.email == 'test@test.com'


def test_service_create_tweet(session):
    user_repo = repositories.UserRepository(session)
    services.create_user(
        user_repo=user_repo,
        username='test',
        email='test@test.com',
    )
    tweet_repo = repositories.TweetRepository(session)
    dto = services.create_tweet(
        tweet_repo=tweet_repo,
        user_repo=user_repo,
        user_id=1,
        content='test message',
    )
    assert dto.tweet_id == 1
    assert dto.username == 'test'
    assert dto.content == 'test message'
