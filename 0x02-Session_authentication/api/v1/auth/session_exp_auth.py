#!/usr/bin/env python3
"""A session expiration implementation"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """A SessionExpAuth class"""

    def __init__(self):
        """Instantiate an object with attributes"""
        # super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID"""
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve a user_id for a session_id"""
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)

        if session_dictionary is None:
            return None

        user_id = session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')

        if user_id is None or created_at is None:
            return None

        if self.session_duration > 0:
            expiration_time = created_at + timedelta(seconds=self.session_duration)
            if datetime.now() > expiration_time:
                return None

        return user_id
