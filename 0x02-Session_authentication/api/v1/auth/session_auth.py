#!/usr/bin/env python3
"""Implements Session Authentication class"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """A SessionAuth class that inherit from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates session id for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves session_id based on user_id"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns an instance of User"""
        cooky = super().session_cookie(request)
        u_id = self.user_id_for_session_id(cooky)
        user = User.get(u_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """Deletes user session id"""
        if request is None:
            return False
        if id not in request.args:
            return False
        sess_id = self.user_id_for_session_id()
        if sess_id is None:
            return False
