#!/usr/bin/env python3
"""A basic authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """A class for Auth"""
    def require_auth(
            self,
            path: str, excluded_paths: List[str]
            ) -> bool:
        """Validates if authentication is needed"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return a user instance"""
        return None
