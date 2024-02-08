#!/usr/bin/env python3
"""password encryption"""

import bcrypt


def hash_password(password: str) -> bytes:
    """password hashing function"""
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a provided password matches bcrypt hashes"""
    password = password.encode('utf-8')
    return bcrypt.checkpwd(password, hashed_password)
