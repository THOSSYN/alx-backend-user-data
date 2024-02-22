#!/usr/bin/env python3
"""A flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root():
    """Defines the root of the app"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Defines a user registration portal"""
    user_email = request.form.get('email')
    user_pass = request.form.get('password')

    try:
        registered_user = AUTH.register_user(user_email, user_pass)
        return jsonify({'email': user_email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    This Method validates login and sends the session_id as cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    log_stat = AUTH.valid_login(email, password)

    if log_stat:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    This method resolves the logout request and invalidates
    the session_id of the user.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
        # return redirect(url_for('home'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    This function resolves the request to find a user.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = jsonify({"email": user.email})
        return response, 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """A route for getting reset token
    """
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            if reset_token:
                return jsonify({"email": email, "reset_token": reset_token})
            abort(403)
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Defines an endpoint for password change"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify(
                    {"email": email, "message": "Password updated"}
                    ), 200
        except (NoResultFound, ValueError):
            abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
