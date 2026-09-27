from datetime import date
from decimal import Decimal

from app.models.employee import Employee
from app.repositories.employee_repository import (
    EmployeeRepository
)

class EmployeeService:

    @staticmethod
    def create_employee(data):

        employee_code = data[
            "employee_code"
        ]

        email = data[
            "email"
        ]

        user_id = data[
            "user_id"
        ]

        if EmployeeRepository.exists_by_employee_code(
            employee_code
        ):

            raise ValueError(
                "Employee code already exists"
            )

        if EmployeeRepository.exists_by_email(
            email
        ):

            raise ValueError(
                "Employee email already exists"
            )

        existing_employee = (
            EmployeeRepository.get_by_user_id(
                user_id
            )
        )

        if existing_employee:

            raise ValueError(
                "An employee record already exists for this user"
            )

        employee = Employee(
            user_id=user_id,
            employee_code=employee_code,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=email,
            phone=data.get("phone"),
            designation=data["designation"],
            salary=data.get("salary"),
            joining_date=date.fromisoformat(
                data["joining_date"]
            ),
            department=data.get(
                "department"
            ),
            is_active=data.get(
                "is_active",
                True
            )
        )

        return EmployeeRepository.create(
            employee
        )

    @staticmethod
    def get_employee(employee_id):

        return EmployeeRepository.get_by_id(
            employee_id
        )

    @staticmethod
    def get_all_employees(
        page=1,
        per_page=10,
        search=None,
        department=None,
        is_active=None
    ):
        return EmployeeRepository.get_all(
            page=page,
            per_page=per_page,
            search=search,
            department=department,
            is_active=is_active
        )

    @staticmethod
    def update_employee(
        employee_id,
        data
    ):

        employee = (
            EmployeeRepository.get_by_id(
                employee_id
            )
        )

        if not employee:

            return None

        if "employee_code" in data:

            employee_code = data[
                "employee_code"
            ]

            existing = (
                EmployeeRepository
                .get_by_employee_code(
                    employee_code
                )
            )

            if existing and existing.id != employee.id:

                raise ValueError(
                    "Employee code already exists"
                )

            employee.employee_code = (
                employee_code
            )

        if "email" in data:

            email = data["email"]

            existing = (
                EmployeeRepository
                .get_by_email(email)
            )

            if existing and existing.id != employee.id:

                raise ValueError(
                    "Employee email already exists"
                )

            employee.email = email

        if "first_name" in data:

            employee.first_name = (
                data["first_name"]
            )

        if "last_name" in data:

            employee.last_name = (
                data["last_name"]
            )

        if "phone" in data:

            employee.phone = (
                data["phone"]
            )

        if "designation" in data:

            employee.designation = (
                data["designation"]
            )

        if "salary" in data:

            employee.salary = (
                Decimal(str(data["salary"]))
            )

        if "joining_date" in data:

            employee.joining_date = (
                date.fromisoformat(
                    data["joining_date"]
                )
            )

        if "department" in data:

            employee.department = (
                data["department"]
            )

        if "is_active" in data:

            employee.is_active = (
                data["is_active"]
            )

        return EmployeeRepository.update(
            employee
        )

    @staticmethod
    def delete_employee(
        employee_id
    ):

        employee = (
            EmployeeRepository.get_by_id(
                employee_id
            )
        )

        if not employee:

            return None

        EmployeeRepository.delete(
            employee
        )

        return employee