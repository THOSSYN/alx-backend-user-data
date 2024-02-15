#!/usr/bin/env python3
"""Routes all session requiring authentications"""

from flask import jsonify, request, session
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate_session():
    """Handles all routes for session authentication"""
    try:
        email_data = request.form.get('email')
        if not email_data:
            return jsonify({"error": "email missing"}), 400

        pwd_data = request.form.get('password')
        if not pwd_data:
            return jsonify({"error": "password missing"}), 400

        users = User.search({"email": email_data})

        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        user = users[0]

        if not user.is_valid_password(pwd_data):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        sess_id = auth.create_session(user.id)

        response = jsonify(user.to_json())
        response.set_cookie(auth._my_session_id, sess_id)
        # session[auth._my_session_id] = sess_id

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
