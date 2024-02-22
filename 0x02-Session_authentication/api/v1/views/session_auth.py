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
        check_user = User.all()
        print(type(check_user))
        for item in check_user:
            print(item.id)
        user1 = User.get('f8206efc-f19f-4c46-aca4-594aadb82ae0')
        print(user1.email)
        print(type(users))

        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        for u in users:
            print(u.id)

        user = users[0]

        if not user.is_valid_password(pwd_data):
            print(f"{user}: error here")
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        from api.v1.auth.session_auth import SessionAuth
        print(f"user_id: {user.id}")
        print(type(user.id))
        sa = SessionAuth()
        sess_id = sa.create_session(user.id)
        if sess_id is None:
            return None
        print(f"{sess_id}: Got here")

        response = jsonify(user.to_json())
        response.set_cookie(auth._my_session_id, sess_id)
        # session[auth._my_session_id] = sess_id

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/auth_session/logout', methods=['DELETE'],
        strict_slashes=False)
def logout():
    """A method for log out"""
    from api.v1.app import auth
    sess_destroyer = auth.destroy_session(request)

    if sess_destroyer == False:
    	abort(404)

    return jsonify({}), 200
