#!/usr/bin/env python3
"""A basic authentication"""

from flask import request
from typing import List, TypeVar
import fnmatch


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
        # add slash if path has no '/' at the end
        if not path.endswith('/'):
            path = path + '/'

        # check if path is in excluded_paths
        for exc_path in excluded_paths:
            if fnmatch.fnmatch(path, exc_path):
                return False
            # allows '*' wildcard in excluded_paths
            if exc_path.endswith('*') and fnmatch.fnmatch(path, exc_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header"""
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Return a user instance"""
        return None
