#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


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

    def add_user(
            self,
            email: str,
            hashed_password: str
            ) -> User:
        """Add a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        if user:
            self._session.add(user)
            self._session.commit()
            return user
        return None

    def find_user_by(self, **kwargs) -> User:
        """
        This method finds a user based on the kwargs parameters passed, and
        returns the user.
        A NoResultFound exception is raised if no result is found, while
        A InvalidRequestError is raised if the query has the wrong arguments.
        """
        session = self._session
        try:
            # filtering is achieved with filter_by, which uses keyword args
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except (NoResultFound) as err:
            raise err
        except (InvalidRequestError) as err:
            raise err
