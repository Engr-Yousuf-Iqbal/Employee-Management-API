from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
    )

def jwt_required_custom():
    def decorator(function):
        
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                if not claims.get("is_active",False):

                    return jsonify({
                        "success": False,
                        "message": "User account is inactive"
                    }), 403
                
                return function(*args, **kwargs)
            
            except Exception:
                return jsonify({
                    "success": False,
                    "message": "Authentication required"
                }), 401
        return wrapper
    
    return decorator

def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            try:
                verify_jwt_in_request()
                claims = get_jwt()
                if not claims.get(
                    "is_active",
                    False
                ):
                    return jsonify({
                        "success": False,
                        "message": "User account is inactive"
                    }), 403
                user_role = claims.get("role")

                if user_role not in allowed_roles:

                    return jsonify({
                        "success": False,
                        "message": "Insufficient permissions"
                    }), 403
                return function(*args, **kwargs)
            except Exception:
                return jsonify({
                    "success": False,
                    "message": "Authorization required"
                }), 403
        
        return wrapper
    return decorator