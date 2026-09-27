from flask import Blueprint

from app.controllers.audit_controller import AuditController
from app.middleware.auth import role_required


audit_bp = Blueprint(
    "audit",
    __name__
)


@audit_bp.route("", methods=["GET"])
@role_required("Admin")
def get_audit_logs():

    return AuditController.get_all()


@audit_bp.route("/user/<int:user_id>", methods=["GET"])
@role_required("Admin")
def get_user_audit_logs(user_id):

    return AuditController.get_by_user(
        user_id
    )