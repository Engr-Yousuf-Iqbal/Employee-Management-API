from flask import (
    request,
    jsonify
)

from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity
)

from app.schemas.employee_schema import (
    EmployeeSchema
)

from app.services.employee_service import (
    EmployeeService
)

from app.services.audit_service import AuditService


class EmployeeController:

    @staticmethod
    def _serialize_employee(employee):

        return {
            "id": employee.id,
            "user_id": employee.user_id,
            "employee_code": employee.employee_code,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "phone": employee.phone,
            "designation": employee.designation,
            "salary": (
                float(employee.salary)
                if employee.salary is not None
                else None
            ),
            "joining_date": (
                employee.joining_date.isoformat()
                if employee.joining_date
                else None
            ),
            "department": employee.department,
            "is_active": employee.is_active,
            "created_at": (
                employee.created_at.isoformat()
            ),
            "updated_at": (
                employee.updated_at.isoformat()
            )
        }

    @staticmethod
    def _is_owner(employee):

        user_id = get_jwt_identity()

        return employee.user_id == int(
            user_id
        )

    @staticmethod
    def create():

        data = request.get_json(
            silent=True
        )

        errors = (
            EmployeeSchema
            .validate_create(data)
        )

        if errors:

            return jsonify({
                "success": False,
                "errors": errors
            }), 400

        try:

            employee = (
                EmployeeService
                .create_employee(data)
            )

            AuditService.log(
                user_id=int(get_jwt_identity()),
                action="CREATE",
                resource="EMPLOYEE",
                resource_id=employee.id,
                description=f"Employee {employee.employee_code} created",
                ip_address=request.remote_addr
            )

            return jsonify({
                "success": True,
                "message": "Employee created successfully",
                "data": EmployeeController
                ._serialize_employee(employee)
            }), 201

        except ValueError as error:

            return jsonify({
                "success": False,
                "message": str(error)
            }), 409

    @staticmethod
    def get_all():

        page=request.args.get(
            "page",
            default=1,
            type=int
        )

        per_page=request.args.get(
            "per_page",
            default=10,
            type=int
        )

        search = request.args.get(
            "search",
            default=None,
            type=str
        )

        department = request.args.get(
            "department",
            default=None,
            type=str
        )

        is_active_param = request.args.get(
            "is_active",
            default=None,
            type=str
        )

        if page < 1:
            return jsonify({
            "success": False,
            "message": "page must be at least 1"
            }),400
        
        if per_page < 1 or per_page > 100:

            return jsonify({
                "success": False,
                "message": "per_page must be between 1 and 100"
            }),400
        
        is_active=None

        if is_active_param is not None:
            if is_active_param.lower() =="true":
                is_active = True
            
            elif is_active_param.lower() == "flase":
                is_active = False

            else:

                return jsonify({
                    "success": False,
                    "message": "is_active must be true or false"
                }), 400
            
        pagination = EmployeeService.get_all_employees(
            page=page,
            per_page=per_page,
            search=search,
            department=department,
            is_active=is_active
        )

        return jsonify({
            "success": True,
            "data": [
                EmployeeController._serialize_employee(employee)
                for employee in pagination.items
            ],
            "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_previous": pagination.has_prev
            } 
        }), 200

    @staticmethod
    def get_by_id(
        employee_id
    ):

        employee = (
            EmployeeService
            .get_employee(employee_id)
        )

        if not employee:

            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        claims = get_jwt()

        role = claims.get(
            "role"
        )

        if role == "Employee":

            if not EmployeeController._is_owner(
                employee
            ):

                return jsonify({
                    "success": False,
                    "message": "Insufficient permissions"
                }), 403

        return jsonify({
            "success": True,
            "data": EmployeeController
            ._serialize_employee(employee)
        }), 200

    @staticmethod
    def update(
        employee_id
    ):

        employee = (
            EmployeeService
            .get_employee(employee_id)
        )

        if not employee:

            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        claims = get_jwt()

        role = claims.get(
            "role"
        )

        if role == "Employee":

            if not EmployeeController._is_owner(
                employee
            ):

                return jsonify({
                    "success": False,
                    "message": "Insufficient permissions"
                }), 403

        data = request.get_json(
            silent=True
        )

        errors = (
            EmployeeSchema
            .validate_update(data)
        )

        if errors:

            return jsonify({
                "success": False,
                "errors": errors
            }), 400

        try:

            updated_employee = (
                EmployeeService
                .update_employee(
                    employee_id,
                    data
                )
            )

            AuditService.log(
                user_id=int(get_jwt_identity()),
                action="UPDATE",
                resource="EMPLOYEE",
                resource_id=employee.id,
                description=f"Employee {employee.employee_code} updated",
                ip_address=request.remote_addr
            )

            return jsonify({
                "success": True,
                "message": "Employee updated successfully",
                "data": EmployeeController
                ._serialize_employee(
                    updated_employee
                )
            }), 200

        except ValueError as error:

            return jsonify({
                "success": False,
                "message": str(error)
            }), 409

    @staticmethod
    def delete(
        employee_id
    ):

        employee = (
            EmployeeService
            .get_employee(employee_id)
        )

        if not employee:

            return jsonify({
                "success": False,
                "message": "Employee not found"
            }), 404

        deleted_employee = (
            EmployeeService
            .delete_employee(
                employee_id
            )
        )

        AuditService.log(
            user_id=int(get_jwt_identity()),
            action="DELETE",
            resource="EMPLOYEE",
            resource_id=employee.id,
            description=f"Employee {employee.employee_code} deleted",
            ip_address=request.remote_addr
        )

        return jsonify({
            "success": True,
            "message": "Employee deleted successfully",
            "data": {
                "id": deleted_employee.id,
                "employee_code": (
                    deleted_employee.employee_code
                )
            }
        }), 200