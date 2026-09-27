from flask import request, jsonify
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from app.middleware.auth import (
    jwt_required_custom,
    role_required
) 
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)

from app.services.audit_service import AuditService


class UserController:
    @staticmethod
    def register():
        data =request.get_json()
        errors = UserSchema.validate_registration(data)
        if errors:
            return jsonify({
                "success":False,
                "errors": errors 
            }), 400
        
        try:
            user = UserService.register_user(
                username= data["username"],
                email= data["email"],
                password= data["password"]
            )
            return jsonify({
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "role":"Employee",
                    "is_active":user.is_active,
                    "created_at":user.created_at.isoformat()
                }
            }),201
        except ValueError as error:
            return jsonify({
                "success":False,
                "message": str(error)
            }),409
    
    @staticmethod
    def login():
        data = request.get_json()

        errors = UserSchema.validate_login(data)
        if errors:
            return errors , 400 
        
        user = UserService.authenticate_user(
            username=data["username"],
            password=data["password"]
        )
        
        if not user:
            return jsonify({
                "Success":False,
                "message": "Invalid username or password"
            }),401
        
        # JWT identity
        identity = str(user.id)
        
        # Additional JWT claims
        claims = {
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active
        }


        access_token = create_access_token(
            identity=identity,
            additional_claims=claims
        )

        refresh_token = create_refresh_token(
            identity=identity,
            additional_claims= claims
        )

        AuditService.log(
        user_id=user.id,
        action="LOGIN",
        resource="USER",
        resource_id=user.id,
        description="User logged in successfully",
        ip_address=request.remote_addr
        )

        return jsonify({
            "success":True,
            "message": "Login successful",
            "data":{
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user":{
                "id": user.id,
                "username":user.username,
                "email":user.email,
                "role":user.role
                }
            }
        }), 200
    
    @staticmethod
    @jwt_required_custom()
    def me():
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(
            int(user_id)
        )
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data":{
                "id":user.id,
                "username":user.username,
                "email":user.email,
                "role": user.role,
                "is_active": user.is_active
            }
        }), 200
    
    @staticmethod
    @jwt_required(refresh=True)
    def refresh():

        user_id = get_jwt_identity()

        user = UserService.get_user_by_id(
            int(user_id)
        )

        if not user:
            return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

        if not user.is_active:

            return jsonify({
                "Success": False,
                "message": "User account is inactive"
            }),403
        
        claims = {
            "username": user.username,
            "role": user.role,
            "is_active": user.is_active
        }

        access_token =create_access_token(
            identity = str(user.id),
            additional_claims= claims
        )

        return jsonify({
            "success": True,
            "message": "Access token refreshed",
            "data": {
                "access_token": access_token
            }
        }), 200


    @staticmethod
    @role_required("Admin")
    def admin_dashboard():

        return jsonify({
            "success": True,
            "message": "welcome Admin",
            "data": {
                "role": "admin"
            }
        }), 200
    
    @staticmethod
    @role_required("Admin", "Manager")
    def Management_dashboard():

        return jsonify({
            "success": True,
            "message": "welcome Management",
            "data": {
                "allowed_roles": (
                    "admin",
                    "Manager"
                )
            }
        }), 200
    
    @staticmethod
    @role_required("Admin", "Manager", "Employee")
    def Authorized_dashboard():

        return jsonify({
            "success": True,
            "message": "Authorized role granted",
        }), 200
    
    
