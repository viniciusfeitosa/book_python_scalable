import model
from typing import Sequence
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UserRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add(self, user: model.User) -> None:
        async with self.session() as session:
            async with session.begin():
                session.add(user)

    async def get_by_username(self, username: str) -> Optional[model.User]:
        async with self.session() as session:
            result = await session.execute(
                select(model.User).filter_by(username=username)
            )
            return result.scalars().first()

    async def get_by_email(self, email: model.Email) -> Optional[model.User]:
        async with self.session() as session:
            result = await session.execute(
                select(model.User).filter_by(email=email)
            )
            return result.scalars().first()

    async def list_all(self) -> Sequence[model.User]:
        async with self.session() as session:
            result = await session.execute(select(model.User))
            return result.scalars().all()


class TweetRepository:

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def add(self, tweet: model.Tweet) -> None:
        async with self.session() as session:
            async with session.begin():
                session.add(tweet)

    async def get_by_id(self, tweet_id: int) -> Optional[model.Tweet]:
        async with self.session() as session:
            result = await session.execute(
                select(model.Tweet).filter_by(id=tweet_id)
            )
            return result.scalar_one_or_none()

    async def list_all(self) -> Sequence[model.Tweet]:
        async with self.session() as session:
            result = await session.execute(
                select(model.Tweet)
            )
            return result.scalars().all()
