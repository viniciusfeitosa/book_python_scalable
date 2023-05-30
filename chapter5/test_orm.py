import domain
from sqlalchemy import text


def test_load_email(session):
    session.execute(
        text('''INSERT INTO emails (address) VALUES
        ("test1@test.com"),
        ("test2@test.com"),
        ("test3@test.com")''')
    )
    expected = [
        domain.Email("test1@test.com"),
        domain.Email("test2@test.com"),
        domain.Email("test3@test.com"),
    ]
    assert session.query(domain.Email).all() == expected


def test_create_email(session):
    e = domain.Email("test_create1@test.com")
    session.add(e)
    session.commit()
    assert session.query(domain.Email).first() == e


def test_load_user(session):
    session.execute(
        text('''INSERT INTO users (username, email) VALUES
        ("test1", "test1@test.com"),
        ("test2", "test2@test.com"),
        ("test3", "test3@test.com")''')
    )
    expected = [
        domain.User('test1', 'test1@test.com'),
        domain.User('test2', 'test2@test.com'),
        domain.User('test3', 'test3@test.com'),
    ]
    assert session.query(domain.User).all() == expected


def test_create_user(session):
    u = domain.User('test1', 'test1@test.com')
    session.add(u)
    session.commit()
    assert session.query(domain.User).first() == u


def test_user_following(session):
    user_1 = domain.User('test1', 'test1@test.com')
    user_2 = domain.User('test2', 'test1@test.com')
    user_3 = domain.User('test3', 'test1@test.com')

    user_1.follow(user_2)
    user_1.follow(user_3)
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()
    query = session.query(domain.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 2
    assert user_2, user_3 in query.following
    assert len(query.followers) == 0


def test_user_followers(session):
    user_1 = domain.User('test1', 'test1@test.com')
    user_2 = domain.User('test2', 'test1@test.com')
    user_3 = domain.User('test3', 'test1@test.com')

    user_2.follow(user_1)
    user_3.follow(user_1)
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()
    query = session.query(domain.User).filter_by(id=user_1.id).one()
    assert len(query.followers) == 2
    assert user_2, user_3 in query.followers
    assert len(query.following) == 0


def test_user_unfollow(session):
    user_1 = domain.User('test1', 'test1@test.com')
    user_2 = domain.User('test2', 'test1@test.com')

    user_1.follow(user_2)
    session.add(user_1)
    session.add(user_2)
    session.commit()
    query = session.query(domain.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 1
    assert user_2 in query.following
    assert len(query.followers) == 0

    user_1.unfollow(user_2)
    session.commit()

    query = session.query(domain.User).filter_by(id=user_1.id).one()
    assert len(query.following) == 0
    assert user_2 not in query.following
    assert len(query.followers) == 0


def test_create_tweet(session):
    user_1 = domain.User('test1', 'test1@test.com')
    session.add(user_1)
    session.commit()

    t1 = domain.Tweet(user_1, 'it is a first test')
    t2 = domain.Tweet(user_1, 'it is a second test')
    session.add(t1)
    session.add(t2)
    session.commit()
    expected = [t1, t2]

    assert session.query(domain.Tweet).all() == expected


def test_like_dislike_tweet(session):
    user_1 = domain.User('test1', 'test1@test.com')
    user_2 = domain.User('test2', 'test2@test.com')
    user_3 = domain.User('test3', 'test3@test.com')
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()

    t1 = domain.Tweet(user_1, 'it is a test')
    t1.like(user_2)
    t1.like(user_3)
    session.add(t1)
    session.commit()
    query = session.query(domain.Tweet).first()
    assert len(query.likes) == 2
    assert user_2, user_3 in query.likes

    t1.unlike(user_2)
    session.commit()
    query = session.query(domain.Tweet).first()
    assert len(query.likes) == 1
    assert user_3 in query.likes
    assert user_2 not in query.likes
