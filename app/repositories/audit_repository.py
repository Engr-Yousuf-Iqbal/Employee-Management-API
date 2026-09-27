from app.config.database import db
from app.models.audit_log import AuditLog


class AuditRepository:

    @staticmethod
    def create(audit_log):
        db.session.add(audit_log)
        db.session.commit()
        return audit_log

    @staticmethod
    def get_all():
        return AuditLog.query.order_by(
            AuditLog.created_at.desc()
        ).all()

    @staticmethod
    def get_by_user_id(user_id):
        return AuditLog.query.filter_by(
            user_id=user_id
        ).order_by(
            AuditLog.created_at.desc()
        ).all()