#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

auth_type = getenv("AUTH_TYPE")

if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
else:
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
# app.secret_key = auth._my_session_id

@app.before_request
def before_request():
    """Verify user's credential before each request"""
    if auth is None:
        return
    excluded = ['/api/v1/stat*', '/api/v1/unauthorized/',
                '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    request.current_user = auth.current_user(request)

    ret_value = auth.require_auth(request.path, excluded)
    if ret_value is False:
        return

    auth_header = auth.authorization_header(request)
    if auth_header is None:
        abort(401)

    auth_session = auth.session_cookie(request)
    if auth_session is None and auth_header is None:
        abort(401)

    auth_user = auth.current_user(request)
    if auth_user is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handle 401 error"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handles 403 error"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
