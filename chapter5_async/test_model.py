import pytest
import model
from sqlalchemy import text, select


@pytest.mark.asyncio
async def test_load_email(session):
    async with session() as ses:
        await ses.execute(
            text('''INSERT INTO emails (address) VALUES
            ("test1@test.com"),
            ("test2@test.com"),
            ("test3@test.com")''')
        )
        expected = [
            model.Email("test1@test.com"),
            model.Email("test2@test.com"),
            model.Email("test3@test.com"),
        ]
        result = await ses.execute(
            select(model.Email)
        )
        assert result.scalars().all() == expected


@pytest.mark.asyncio
async def test_create_email(session):
    e = model.Email("test_create1@test.com")
    async with session() as ses:
        async with ses.begin():
            ses.add(e)
        result = await ses.execute(
            select(model.Email)
        )
        assert result.scalars().first() == e


@pytest.mark.asyncio
async def test_load_user(session):
    async with session() as ses:
        await ses.execute(
            text('''INSERT INTO users (username, email) VALUES
            ("test1", "test1@test.com"),
            ("test2", "test2@test.com"),
            ("test3", "test3@test.com")''')
        )
        expected = [
            model.User('test1', 'test1@test.com'),
            model.User('test2', 'test2@test.com'),
            model.User('test3', 'test3@test.com'),
        ]
        result = await ses.execute(
            select(model.User)
        )
        assert result.scalars().all() == expected


@pytest.mark.asyncio
async def test_create_user(session):
    u = model.User('test1', 'test1@test.com')
    async with session() as ses:
        async with ses.begin():
            ses.add(u)
        result = await ses.execute(
            select(model.User)
        )
        assert result.scalars().first() == u


@pytest.mark.asyncio
async def test_user_following(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')
    user_1.follow(user_2)
    user_1.follow(user_3)
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(user_2)
            ses.add(user_3)
        query = await ses.execute(
            select(model.User).filter_by(id=user_1.id)
        )
        result = query.scalars().one()
        assert len(result.following) == 2
        assert user_2, user_3 in result.following
        assert len(result.followers) == 0


@pytest.mark.asyncio
async def test_user_followers(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')
    user_2.follow(user_1)
    user_3.follow(user_1)
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(user_2)
            ses.add(user_3)
        query = await ses.execute(
            select(model.User).filter_by(id=user_1.id)
        )
        result = query.scalars().one()
        assert len(result.followers) == 2
        assert user_2, user_3 in result.followers
        assert len(result.following) == 0


@pytest.mark.asyncio
async def test_user_unfollow(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')

    user_1.follow(user_2)
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(user_2)
        query = await ses.execute(
            select(model.User).filter_by(id=user_1.id)
        )
        result = query.scalars().one()
        assert len(result.following) == 1
        assert user_2 in result.following
        assert len(result.followers) == 0

        user_1.unfollow(user_2)

        query = await ses.execute(
            select(model.User).filter_by(id=user_1.id)
        )
        result = query.scalars().one()
        assert len(result.following) == 0
        assert user_2 not in result.following
        assert len(result.followers) == 0


@pytest.mark.asyncio
async def test_create_tweet(session):
    user_1 = model.User('test1', 'test1@test.com')
    t1 = model.Tweet(user_1, 'it is a first test')
    t2 = model.Tweet(user_1, 'it is a second test')
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(t1)
            ses.add(t2)
        expected = [t1, t2]
        result = await ses.execute(
            select(model.Tweet)
        )
        assert result.scalars().all() == expected


@pytest.mark.asyncio
async def test_like_dislike_tweet(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_3 = model.User('test3', 'test3@test.com')
    t1 = model.Tweet(user_1, 'it is a test')
    t1.like(user_2)
    t1.like(user_3)
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(user_2)
            ses.add(user_3)
            ses.add(t1)
        query = await ses.execute(
            select(model.Tweet)
        )
        result = query.scalars().first()
        assert len(result.likes) == 2
        assert user_2, user_3 in result.likes

        t1.unlike(user_2)
        query = await ses.execute(
            select(model.Tweet)
        )
        result = query.scalars().first()
        assert len(result.likes) == 1
        assert user_3 in result.likes
        assert user_2 not in result.likes


@pytest.mark.asyncio
async def test_feed(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')
    user_1.follow(user_2)
    t1 = model.Tweet(user_1, 'it my on message')
    t2 = model.Tweet(user_2, 'it is the first user_1 message')
    t3 = model.Tweet(user_2, 'it is the second user_1 message')
    async with session() as ses:
        async with ses.begin():
            ses.add(user_1)
            ses.add(user_2)
            ses.add(t1)
            ses.add(t2)
            ses.add(t3)
        query_user_1 = await ses.execute(
            select(model.User).filter_by(id=user_1.id)
        )
        result_user_1 = query_user_1.scalars().one()
        query_user_2 = await ses.execute(
            select(model.User).filter_by(id=user_2.id)
        )
        result_user_2 = query_user_2.scalars().one()
        assert len(result_user_1.get_feed()) == 3
        assert len(result_user_2.get_feed()) == 2
        assert isinstance(result_user_1.get_feed()[0], model.TweetDTO)
        assert result_user_1.get_feed()[0].content == t3.content
