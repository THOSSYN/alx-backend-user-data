#!/usr/bin/env python3
"""Authentication implemantation"""
import bcrypt
from db import DB
from user import User
import uuid
from typing import Union, TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Password hashing logic"""
    encoded_pwd = password.encode('utf-8')
    salt_algo = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_pwd, salt_algo)


def _generate_uuid() -> str:
    """Generates a uuid identification"""
    return str(uuid.uuid4())


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

            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates users login details
           Return: True if user exist else False
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            encode_pwd = password.encode('utf-8')
            result = bcrypt.checkpw(encode_pwd, existing_user.hashed_password)
            return result
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session"""
        try:
            existing_user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(existing_user.id, session_id=sess_id)
            # setattr(existing_user, 'session_id', sess_id)
            self._db._session.commit()
            return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self,
            session_id: str) -> Union[TypeVar('User'), None]:
        """Retrieves user's session id"""
        if session_id is None:
            return None

        try:
            user_exist = self._db.find_user_by(session_id=session_id)
            # if session_id is None or user_exist is None:
            return user_exist
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys session id for a user by updating
           the session id to None
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Set the reset_token attribute of the user in
        the database.
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
            except NoResultFound:
                raise ValueError

        return None

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password for user"""
        if reset_token:
            try:
                user = self._db.find_user_by(reset_token=reset_token)
                new_hash = _hash_password(password)
                self._db.update_user(user.id, hashed_password=new_hash)
                self._db.update_user(user.id, reset_token=None)
            except NoResultFound:
                raise ValueError
            except ValueError as error:
                raise error
