#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        if email and hashed_password:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        return None

    def find_user_by(self, **kwargs) -> str:
        """Filter user by keyword argument(attributes)"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except (InvalidRequestError) as err:
            raise err
        except (NoResultFound) as err:
            raise err

    def update_user(self, user_id: str, **kwargs) -> None:
        """Update a user object"""
        found_user = self.find_user_by(id=user_id)
        if not found_user:
            return None
        if not kwargs:
            raise ValueError("Attribute does not exist")

        for k, v in kwargs.items():
            if not hasattr(found_user, k):
                raise ValueError(f"Attribute {k} does not exist")
            setattr(found_user, k, v)
        self._session.commit()


def _hash_password(self, password: str) -> bytes:
    """Password-hashing method"""
    encoded_pwd = password.encode('utf-8')
    salt_algo = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_pwd, salt_algo)
