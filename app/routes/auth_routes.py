from flask import Blueprint
from app.controllers.user_controller import UserController

auth_bp = Blueprint("auth",__name__)

auth_bp.route(
    "/refresh",
    methods=["POST"]
)(
    UserController.refresh
)