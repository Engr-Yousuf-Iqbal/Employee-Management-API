from flask import Blueprint

from app.controllers.employee_controller import (
    EmployeeController
)

from app.middleware.auth import (
    jwt_required_custom,
    role_required
)


employee_bp = Blueprint(
    "employees",
    __name__
)


# CREATE
@employee_bp.route(
    "",
    methods=["POST"]
)
@role_required(
    "Admin",
    "Manager"
)
def create_employee():

    """
    Create a new employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:
      - in: body
        name: employee
        required: true
        schema:
          type: object
          required:
            - user_id
            - employee_code
            - first_name
            - last_name
            - email
            - designation
            - joining_date
          properties:
            user_id:
              type: integer
              example: 1
            employee_code:
              type: string
              example: EMP001
            first_name:
              type: string
              example: Muhammad
            last_name:
              type: string
              example: Yousaf
            email:
              type: string
              example: employee@example.com
            phone:
              type: string
              example: "+923001234567"
            designation:
              type: string
              example: Software Engineer
            salary:
              type: number
              example: 150000
            joining_date:
              type: string
              format: date
              example: "2026-09-18"
            department:
              type: string
              example: IT
            is_active:
              type: boolean
              example: true

    responses:
      201:
        description: Employee created successfully

      400:
        description: Validation error

      401:
        description: Authentication required

      403:
        description: Insufficient permissions

      409:
        description: Duplicate employee data
    """

    return EmployeeController.create()


# GET ALL
@employee_bp.route(
    "",
    methods=["GET"]
)
@role_required(
    "Admin",
    "Manager"
)
def get_all_employees():

    """
    Get employees
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:

      - name: page
        in: query
        type: integer
        default: 1

      - name: per_page
        in: query
        type: integer
        default: 10

      - name: search
        in: query
        type: string

      - name: department
        in: query
        type: string

      - name: is_active
        in: query
        type: boolean

    responses:

      200:
        description: Employee list

      401:
        description: Authentication required

      403:
        description: Insufficient permissions
    """

    return EmployeeController.get_all()


# GET ONE
@employee_bp.route(
    "/<int:employee_id>",
    methods=["GET"]
)
@jwt_required_custom()
def get_employee(employee_id):

    """
    Get employee by ID
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:
      - name: employee_id
        in: path
        required: true
        type: integer
        example: 1

    responses:

      200:
        description: Employee found

      401:
        description: Authentication required

      403:
        description: Insufficient permissions

      404:
        description: Employee not found
    """

    return EmployeeController.get_by_id(
        employee_id
    )


# UPDATE
@employee_bp.route(
    "/<int:employee_id>",
    methods=["PUT"]
)
@jwt_required_custom()
def update_employee(employee_id):

    """
    Update employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:

      - name: employee_id
        in: path
        required: true
        type: integer
        example: 1

      - in: body
        name: employee
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            email:
              type: string
            phone:
              type: string
            designation:
              type: string
            salary:
              type: number
            joining_date:
              type: string
              format: date
            department:
              type: string
            is_active:
              type: boolean

    responses:

      200:
        description: Employee updated

      400:
        description: Validation error

      401:
        description: Authentication required

      403:
        description: Insufficient permissions

      404:
        description: Employee not found

      409:
        description: Duplicate data
    """

    return EmployeeController.update(
        employee_id
    )


# DELETE
@employee_bp.route(
    "/<int:employee_id>",
    methods=["DELETE"]
)
@role_required(
    "Admin"
)
def delete_employee(employee_id):

    """
    Delete employee
    ---
    tags:
      - Employees

    security:
      - Bearer: []

    parameters:
      - name: employee_id
        in: path
        required: true
        type: integer
        example: 1

    responses:

      200:
        description: Employee deleted

      401:
        description: Authentication required

      403:
        description: Admin access required

      404:
        description: Employee not found
    """

    return EmployeeController.delete(
        employee_id
    )

