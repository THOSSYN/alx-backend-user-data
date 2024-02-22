#!/usr/bin/env python3
"""Authentication implemantation"""
import bcrypt
from db import DB
from user import User
import uuid
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """User registration for new user
           Return: User instance
        """
        try:
            existing_user = self._db.find_user_by(email=email)

            # if existing_user is not None:
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)
            new_user = User(email=email, hashed_password=hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login details"""
        existing_user = self._db.find_user_by(email=email)

        if existing_user:
            encode_pwd = password.encode('utf-8')
            result = bcrypt.checkpw(encode_pwd, existing_user.hashed_password)
            return result
        return False

    def _generate_uuid(self) -> str:
        """Generates a uuid identification"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a session"""
        existing_user = self._db.find_user_by(email=email)
        if existing_user is None:
            return None
        sess_id = self._generate_uuid()
        setattr(existing_user, 'session_id', sess_id)
        self._db._session.commit()
        return sess_id


def _hash_password(password: str) -> bytes:
    """Password hashing logic"""
    encoded_pwd = password.encode('utf-8')
    salt_algo = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_pwd, salt_algo)
