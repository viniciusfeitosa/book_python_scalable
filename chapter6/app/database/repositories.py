from typing import Optional, Protocol

from sqlalchemy.orm import Session

import app.core.model as model


class RepositoryPort(Protocol):
    def add(self, obj: model.Model) -> model.Model:
        ...

    def get_by_id(self, obj_id: int) -> Optional[model.Model]:
        ...

    def list_all(self) -> list[model.Model]:
        ...


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: model.User) -> model.User:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, obj_id: int) -> Optional[model.User]:
        return self.session.query(
            model.User).filter_by(id=obj_id).one_or_none()

    def list_all(self) -> list[model.User]:
        return self.session.query(model.User).all()


class TweetRepository:

    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: model.Tweet) -> model.Tweet:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, obj_id: int) -> Optional[model.Tweet]:
        return self.session.query(
            model.Tweet).filter_by(id=obj_id).one_or_none()

    def list_all(self) -> list[model.Tweet]:
        return self.session.query(model.Tweet).all()
