#!/usr/bin/env python3
"""Implements UserSession"""

from models.base import Base


class UserSession(Base):
    """A UserSession class for persistence"""
    def __init__(self, user_id: str = None, session_id: str = None, *args: list, **kwargs: dict):
        """Instantiate attributes on class object"""
        super().__init__(*args, **kwargs)

        self.user_id = user_id
        self.session_id = session_id

        # Initialize additional attributes dynamically from args
        for attr in args:
            setattr(self, attr, None)

        # Initialize additional attributes from kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)
