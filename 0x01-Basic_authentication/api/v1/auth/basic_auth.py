#!/usr/bin/env python3
"""A Basic Auth implementation"""

from api.v1.auth.auth import Auth
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
        email, pwd = decoded_base64_authorization_header.split(':')
        return email, pwd
