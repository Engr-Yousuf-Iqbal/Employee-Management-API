from flask import Blueprint
from app.controllers.user_controller import UserController

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)

user_bp = Blueprint(
    "users",
    __name__,
)

user_bp.route(
    "/register",
    methods=["POST"]
)(
    UserController.register
)

user_bp.route(
    "/login",
    methods=["POST"]
)(
    limiter.limit("5 per minute")(
    UserController.login
))

user_bp.route(
    "/me",
    methods=["GET"]
)(
    UserController.me
)

user_bp.route(
    "/admin",
    methods=["GET"]
)(
    UserController.admin_dashboard
)

user_bp.route(
    "/management",
    methods=["GET"]
)(
    UserController.Management_dashboard
)

user_bp.route(
    "/authorized",
    methods=["GET"]
)(
    UserController.Authorized_dashboard
)