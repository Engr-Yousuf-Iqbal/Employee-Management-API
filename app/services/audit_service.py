from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository


class AuditService:

    @staticmethod
    def log(
        user_id,
        action,
        resource,
        resource_id=None,
        description=None,
        ip_address=None
    ):

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            description=description,
            ip_address=ip_address
        )

        return AuditRepository.create(
            audit_log
        )

    @staticmethod
    def get_all_logs():
        return AuditRepository.get_all()

    @staticmethod
    def get_user_logs(user_id):
        return AuditRepository.get_by_user_id(
            user_id
        )