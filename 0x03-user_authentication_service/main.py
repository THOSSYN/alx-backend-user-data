#!/usr/bin/env python3
"""A general main function"""

import requests
from auth import Auth

auth = Auth()

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test for register user"""
    expected_response = {'email': email, 'message': 'user created'}
    server_response = requests.post(
        'http://127.0.0.1:5000/users',
        data={'email': email, 'password': password}
    ).json()
    assert expected_response == server_response


def log_in_wrong_password(email: str, password: str) -> None:
    """Check for behaviour when wrong password is used"""
    expected_output = {'message': 'Unauthorized'}
    server_output = requests.post(
            'http://127.0.0.1:5000/sessions',
            data={'email': email, 'password': password}
    ).json()

    assert expected_output == server_output


def log_out(session_id: str) -> None:
    """Test logout route"""
    expected_result = {'message': 'Bienvenue'}
    server_result = requests.delete('http://127.0.0.1:5000/sessions')
    assert ecpected_result == server_result


def log_in(email: str, password: str) -> str:
    """Check for behavior when correct login is used"""
    expected_output = {"email": email, "message": "logged in"}
    server_output = requests.post(
            'http://127.0.0.1:5000/sessions',
            data={'email': email, 'password': password}
    ).json()

    assert expected_output == server_output


def profile_unlogged() -> None:
    """Test profile route"""
    pass


def profile_logged(session_id: str) -> None:
    """Test logged profile route"""
    expected_output = {"email": user.email}
    server_output = requests.get('http://127.0.0.1:5000/profile')
    assert expected_output == server_output


def reset_password_token(email: str) -> str:
    """Reset token for changed password"""
    try:
        reset_token = auth.get_reset_password_token(email)
        return reset_token
    except NoResultFound:
        raise ValueError


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests for password update"""
    expected_response = {"email": email, "message": "Password updated"}
    server_response = requests.put(
            'http://127.0.0.1:5000/reset_password',
            json={
                'email': email,
                'reset_token': reset_token,
                'new_password': new_password}
            ).json()
    assert expected_response == server_response


if __name__ == '__main__':
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
