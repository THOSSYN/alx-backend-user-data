#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


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
            ) -> TypeVar('User'):
        """Add a user to the database"""
        user = User(email, hashed_password)
        seld.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> str:
        """Filter user by keyword argument(attributes)
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("Not found")
            return user
        except InvalidRequestError as e:
            print(e)
            raise InvalidRequestError("Invalid")
        """
        # try:
        user = self._session.query(User).filter_by(**kwargs).first()
        # if user is None:
            # raise ValueError("User Not in DB")
        return user


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