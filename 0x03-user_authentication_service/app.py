#!/usr/bin/env python3
"""A flask app"""
from flask import Flask, jsonify, request, Response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root() -> Response:
    """Defines the root of the app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Response:
    """Defines a user registration portal"""
    user_email = request.form.get('email')
    user_pass = request.form.get('password')

    # found_user = AUTH.find_user(email=email)
    # if found_user:
    # return jsonify({'message': 'email already registered'}), 400

    try:
        registered_user = AUTH.register_user(user_email, user_pass)
        return jsonify({'email': f'{user_email}', 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
