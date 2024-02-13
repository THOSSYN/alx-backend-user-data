#!/usr/bin/env python3
"""A Basic Auth implementation"""

from api.v1.auth.auth import Auth


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
