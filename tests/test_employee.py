import os
import pytest

from app import create_app, db

from app.models.user import User
from app.models.employee import Employee

from flask_jwt_extended import (
    create_access_token
)
from app.utils.password import  hash_password

@pytest.fixture
def app():

    app = create_app()

    app.config.update({
        "TESTING":True,
        "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DB_URI")
    })

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def users(app):

    with app.app_context():

        admin = User(
            username="admin",
            email="admin@example.com",
            role="Admin",
            is_active=True,
            password_hash=hash_password("Admin123")
        )

        manager = User(
            username="manager",
            email="manager@example.com",
            role="Manager",
            is_active=True,
            password_hash=hash_password("Manager123")
        )


        employee = User(
            username="employee",
            email="employee@example.com",
            role="Employee",
            is_active=True,
            password_hash=hash_password("Employee123")
        )


        db.session.add_all([
            admin,
            manager,
            employee
        ])

        db.session.commit()

        return {
            "admin": admin.id,
            "manager": manager.id,
            "employee": employee.id
        }


def get_token(app, user_id, role):

    with app.app_context():

        return create_access_token(
            identity=str(user_id),
            additional_claims={
                "role": role,
                "is_active": True,
                "username": role.lower()
            }
        )


def employee_payload(user_id):

    return {
        "user_id": user_id,
        "employee_code": "EMP001",
        "first_name": "Muhammad",
        "last_name": "Yousaf",
        "email": "employee@test.com",
        "phone": "+923001234567",
        "designation": "Software Engineer",
        "salary": 150000,
        "joining_date": "2026-09-13",
        "department": "IT",
        "is_active": True
    }


def test_admin_can_create_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True


def test_manager_can_create_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["manager"],
        "Manager"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201


def test_employee_cannot_create_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["employee"],
        "Employee"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_manager_can_get_all_employees(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["manager"],
        "Manager"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    response = client.get(
        "/api/v1/employees",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1


def test_employee_cannot_get_all_employees(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["employee"],
        "Employee"
    )

    response = client.get(
        "/api/v1/employees",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_employee_can_get_own_record(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    employee_token = get_token(
        app,
        users["employee"],
        "Employee"
    )

    response = client.get(
        f"/api/v1/employees/{employee_id}",
        headers={
            "Authorization": (
                f"Bearer {employee_token}"
            )
        }
    )

    assert response.status_code == 200


def test_employee_cannot_get_other_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    payload = employee_payload(
        users["manager"]
    )

    response = client.post(
        "/api/v1/employees",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    employee_token = get_token(
        app,
        users["employee"],
        "Employee"
    )

    response = client.get(
        f"/api/v1/employees/{employee_id}",
        headers={
            "Authorization": (
                f"Bearer {employee_token}"
            )
        }
    )

    assert response.status_code == 403


def test_admin_can_update_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    response = client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "designation": "Senior Engineer",
            "salary": 180000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["data"]["designation"]
        == "Senior Engineer"
    )


def test_employee_can_update_own_record(
    app,
    client,
    users
):

    admin_token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": (
                f"Bearer {admin_token}"
            )
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    employee_token = get_token(
        app,
        users["employee"],
        "Employee"
    )

    response = client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "phone": "+923119999999"
        },
        headers={
            "Authorization": (
                f"Bearer {employee_token}"
            )
        }
    )

    assert response.status_code == 200


def test_admin_can_delete_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    response = client.delete(
        f"/api/v1/employees/{employee_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_manager_cannot_delete_employee(
    app,
    client,
    users
):

    admin_token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.post(
        "/api/v1/employees",
        json=employee_payload(
            users["employee"]
        ),
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    employee_id = response.get_json()[
        "data"
    ]["id"]

    manager_token = get_token(
        app,
        users["manager"],
        "Manager"
    )

    response = client.delete(
        f"/api/v1/employees/{employee_id}",
        headers={
            "Authorization": f"Bearer {manager_token}"
        }
    )

    assert response.status_code == 403


def test_get_nonexistent_employee(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    response = client.get(
        "/api/v1/employees/9999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


def test_duplicate_employee_code(
    app,
    client,
    users
):

    token = get_token(
        app,
        users["admin"],
        "Admin"
    )

    payload = employee_payload(
        users["employee"]
    )

    response = client.post(
        "/api/v1/employees",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    second_payload = payload.copy()

    second_payload["user_id"] = users["manager"]
    second_payload["email"] = "another@test.com"

    response = client.post(
        "/api/v1/employees",
        json=second_payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 409