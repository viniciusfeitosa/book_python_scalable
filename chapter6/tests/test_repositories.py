import app.core.model as model
import app.database.repositories as repositories


def test_user_repository(session):
    repo = repositories.UserRepository(session)
    user_created_1 = repo.add(model.User('test1', 'test1@test.com'))
    user_created_2 = repo.add(model.User('test2', 'test2@test.com'))
    assert user_created_1.id == 1
    assert user_created_2.id == 2

    all_users = repo.list_all()
    assert len(all_users) == 2

    user_1 = repo.get_by_id(user_created_1.id)
    assert user_1.username == 'test1'

    user_2 = repo.get_by_id(user_created_2.id)
    assert user_2.username == 'test2'

    user_does_not_exists = repo.get_by_id(3)
    assert user_does_not_exists is None


def test_tweet_repository(session):
    user_1 = model.User('test1', 'test1@test.com')
    user_2 = model.User('test2', 'test2@test.com')

    repo = repositories.TweetRepository(session)
    all_tweets = repo.list_all()
    assert len(all_tweets) == 0

    repo.add(model.Tweet(user_1, 'It is the test1'))
    repo.add(model.Tweet(user_1, 'It is the test2'))
    repo.add(model.Tweet(user_1, 'It is the test3'))
    repo.add(model.Tweet(user_2, 'It is the test4'))
    assert len(user_1.get_feed()) == 3
    assert len(user_2.get_feed()) == 1

    all_tweets = repo.list_all()
    assert len(all_tweets) == 4
    tweet1 = repo.get_by_id(1)
    assert tweet1.user.username == 'test1'
    assert tweet1.content == 'It is the test1'
