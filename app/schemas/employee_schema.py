import re
from datetime import date


class EmployeeSchema:

    @staticmethod
    def validate_create(data):

        errors = {}

        if not data:
            return {
                "error": "Request body is required"
            }

        employee_code = data.get(
            "employee_code"
        )

        first_name = data.get(
            "first_name"
        )

        last_name = data.get(
            "last_name"
        )

        email = data.get(
            "email"
        )

        phone = data.get(
            "phone"
        )

        designation = data.get(
            "designation"
        )

        salary = data.get(
            "salary"
        )

        joining_date = data.get(
            "joining_date"
        )

        department = data.get(
            "department"
        )

        user_id = data.get(
            "user_id"
        )

        # employee code

        if not employee_code:

            errors["employee_code"] = (
                "Employee code is required"
            )

        elif not isinstance(
            employee_code,
            str
        ):

            errors["employee_code"] = (
                "Employee code must be a string"
            )

        elif not re.match(
            r"^[A-Za-z0-9-]+$",
            employee_code
        ):

            errors["employee_code"] = (
                "Employee code contains invalid characters"
            )

        # user id

        if user_id is None:

            errors["user_id"] = (
                "User ID is required"
            )

        elif not isinstance(
            user_id,
            int
        ):

            errors["user_id"] = (
                "User ID must be an integer"
            )

        # first name

        if not first_name:

            errors["first_name"] = (
                "First name is required"
            )

        elif not isinstance(
            first_name,
            str
        ):

            errors["first_name"] = (
                "First name must be a string"
            )

        # last name

        if not last_name:

            errors["last_name"] = (
                "Last name is required"
            )

        elif not isinstance(
            last_name,
            str
        ):

            errors["last_name"] = (
                "Last name must be a string"
            )

        # email

        if not email:

            errors["email"] = (
                "Email is required"
            )

        elif not isinstance(
            email,
            str
        ):

            errors["email"] = (
                "Email must be a string"
            )

        elif not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email
        ):

            errors["email"] = (
                "Invalid email address"
            )

        # phone

        if phone is not None:

            if not isinstance(
                phone,
                str
            ):

                errors["phone"] = (
                    "Phone must be a string"
                )

        # designation

        if not designation:

            errors["designation"] = (
                "Designation is required"
            )

        elif not isinstance(
            designation,
            str
        ):

            errors["designation"] = (
                "Designation must be a string"
            )

        # salary

        if salary is not None:

            if not isinstance(
                salary,
                (int, float)
            ):

                errors["salary"] = (
                    "Salary must be a number"
                )

            elif salary < 0:

                errors["salary"] = (
                    "Salary cannot be negative"
                )

        # joining date

        if not joining_date:

            errors["joining_date"] = (
                "Joining date is required"
            )

        else:

            try:

                date.fromisoformat(
                    joining_date
                )

            except (
                ValueError,
                TypeError
            ):

                errors["joining_date"] = (
                    "Joining date must use YYYY-MM-DD format"
                )

        # department

        if department is not None:

            if not isinstance(
                department,
                str
            ):

                errors["department"] = (
                    "Department must be a string"
                )

        return errors

    @staticmethod
    def validate_update(data):

        errors = {}

        if not data:

            return {
                "error": "Request body is required"
            }

        allowed_fields = {
            "employee_code",
            "first_name",
            "last_name",
            "email",
            "phone",
            "designation",
            "salary",
            "joining_date",
            "department",
            "is_active"
        }

        for field in data:

            if field not in allowed_fields:

                errors[field] = (
                    "Field cannot be updated"
                )

        if "employee_code" in data:

            if not isinstance(
                data["employee_code"],
                str
            ):

                errors["employee_code"] = (
                    "Employee code must be a string"
                )

        if "first_name" in data:

            if not isinstance(
                data["first_name"],
                str
            ):

                errors["first_name"] = (
                    "First name must be a string"
                )

        if "last_name" in data:

            if not isinstance(
                data["last_name"],
                str
            ):

                errors["last_name"] = (
                    "Last name must be a string"
                )

        if "email" in data:

            email = data["email"]

            if not isinstance(
                email,
                str
            ):

                errors["email"] = (
                    "Email must be a string"
                )

            elif not re.match(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                email
            ):

                errors["email"] = (
                    "Invalid email address"
                )

        if "salary" in data:

            salary = data["salary"]

            if not isinstance(
                salary,
                (int, float)
            ):

                errors["salary"] = (
                    "Salary must be a number"
                )

            elif salary < 0:

                errors["salary"] = (
                    "Salary cannot be negative"
                )

        if "joining_date" in data:

            try:

                date.fromisoformat(
                    data["joining_date"]
                )

            except (
                ValueError,
                TypeError
            ):

                errors["joining_date"] = (
                    "Joining date must use YYYY-MM-DD format"
                )

        if "is_active" in data:

            if not isinstance(
                data["is_active"],
                bool
            ):

                errors["is_active"] = (
                    "is_active must be true or false"
                )

        return errors