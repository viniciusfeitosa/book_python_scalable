from typing import Optional

import pytest

from app.core import model, usecases
from app.database import repositories


class FakeUserRepository:
    def add(self, obj: model.Model) -> model.Model:
        obj.id = 1
        return obj

    def get_by_id(self, obj_id: int) -> Optional[model.Model]:
        if obj_id == 1:
            user = model.User('test', 'test@test.com')
            user.id = obj_id
            return user
        return None

    def list_all(self) -> list[model.Model]:
        user = model.User('test', 'test@test.com')
        user.id = 1
        return [user]


def test_service_create_user():
    repo = FakeUserRepository()
    dto = usecases.create_user(
        user_repo=repo,
        username='test',
        email='test@test.com',
    )
    assert dto.user_id == 1
    assert dto.username == 'test'
    assert dto.email == 'test@test.com'


def test_service_get_user_by_id():
    repo = FakeUserRepository()
    with pytest.raises(usecases.UserNotFoundError) as err:
        usecases.get_user_by_id(
            user_repo=repo,
            user_id=2,
        )
    assert str(err.value) == 'Not found user_id: 2'
    dto = usecases.get_user_by_id(
        user_repo=repo,
        user_id=1,
    )
    assert dto.user_id == 1
    assert dto.username == 'test'
    assert dto.email == 'test@test.com'


def test_service_create_tweet(session):
    user_repo = FakeUserRepository()
    tweet_repo = repositories.TweetRepository(session)
    dto = usecases.create_tweet(
        tweet_repo=tweet_repo,
        user_repo=user_repo,
        user_id=1,
        content='test message',
    )
    assert dto.tweet_id == 1
    assert dto.username == 'test'
    assert dto.content == 'test message'
