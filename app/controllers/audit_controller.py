from flask import jsonify

from app.services.audit_service import AuditService


class AuditController:

    @staticmethod
    def get_all():

        logs = AuditService.get_all_logs()

        data = [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "description": log.description,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]

        return jsonify({
            "success": True,
            "data": data
        }), 200

    @staticmethod
    def get_by_user(user_id):

        logs = AuditService.get_user_logs(
            user_id
        )

        data = [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "description": log.description,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]

        return jsonify({
            "success": True,
            "data": data
        }), 200