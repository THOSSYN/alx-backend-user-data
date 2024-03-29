#!/usr/bin/env python3
"""A Basic Auth implementation"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts authorization header from request"""
        if authorization_header is None or \
                not isinstance(authorization_header, str) or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decodes authorization header"""
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except ValueError:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """Extracts decoded authorization header"""
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return None, None
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return email, pwd

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """Return a user object after authentication"""
        if user_email is None or user_pwd is None:
            return None

        users = User.search({"email": user_email})

        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request"""
        if request is None:
            return None

        # Get the Authorization header from the request
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract and decode the Base64 part of the Authorization header
        base64_part = self.extract_base64_authorization_header(auth_header)
        if base64_part is None:
            return None

        # Decode the Base64 part to get the user credentials
        decoded_creds = self.decode_base64_authorization_header(
                base64_part
                )
        if decoded_creds is None:
            return None

        # Extract user email and password from decoded credentials
        user_email, user_pwd = self.extract_user_credentials(
                decoded_creds
                )
        if user_email is None or user_pwd is None:
            return None

        # Authenticate and retrieve the User instance with email
        return self.user_object_from_credentials(user_email, user_pwd)
