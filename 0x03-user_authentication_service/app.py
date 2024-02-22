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
    """Defines a login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    is_valid = AUTH.valid_login(email=email, password=password)
    if is_valid:
        sess_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', sess_id)
        return response
    abort(401)


@app.route('/session', methods=["DELETE"], strict_slashes=False)
def logout():
    """Defines an app logout logic"""
    if request.method == 'DELETE':
        sess_id = request.cookies.get("session_id")
        user_exist = AUTH.get_user_by_session_id(sess_id)

        if user_exist:
            AUTH.destroy_session(user_exist.id)
            return redirect(url_for('/'))
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
