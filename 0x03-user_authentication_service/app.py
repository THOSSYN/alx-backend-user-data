#!/usr/bin/env python3
"""A flask app"""
from flask import Flask, jsonify, request, make_response
from auth import Auth


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

    found_user = AUTH.find_user_by(email=email)

    if found_user:
        sess_id = AUTH.create_session(email)
        response = make_response({"email": email, "message": "logged in"})
        return response.set_cookie('session_id', sess_id)
        return response
    else:
        abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
