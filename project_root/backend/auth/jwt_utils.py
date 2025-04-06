import jwt
from flask import request, jsonify, g
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from backend.db_models import User  
from backend.db import SessionLocal

SECRET_KEY = "your-secret-key"

def token_required(f):
    """
    Decorator to enforce token-based authentication using raw JWT.

    Retrieves the token from the `Authorization` header, decodes it,
    and attaches the authenticated user to Flask's global context `g`.

    Returns:The decorated function if token is valid; otherwise, an error response.
    """
     
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["sub"]
            session = SessionLocal()
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({"message": "User not found"}), 404
            g.current_user = user  # 🟢 this stores current user globally
        except Exception:
            return jsonify({"message": "Token is invalid"}), 401

        return f(*args, **kwargs)
    return decorated


def get_current_user():
    """
    Retrieves the currently authenticated user based on JWT identity.

    Uses Flask-JWT-Extended's `get_jwt_identity()` to fetch user ID and queries the database.

    Returns:
        User instance or None if unauthenticated.
    """
    session = SessionLocal()
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return session.query(User).filter_by(id=user_id).first()