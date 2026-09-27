import os
import pytest

from app import create_app, db
from app.models.user import User
from app.utils.password import hash_password

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
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

def register_user(
        client,
        username="testuser",
        email="test@example.com",
        password="Password234"
):
    return client.post(
        "api/v1/users/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

def create_user_directly(
    username,
    email,
    role,
    password="Password234"
):
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=True
    )

    db.session.add(user)
    db.session.commit()

    return user

def login_user(
        client,
        username="testuser",
        password="Password234"
):
    return client.post(
        "api/v1/users/login",
        json={
            "username": username,
            "password": password
        }
    )


def test_login_returns_access_token(client):
    register_user(client)
    response = login_user(client)

    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert "access_token" in data["data"]

def test_login_return_refresh_token(client):
    
    register_user(client)
    response = login_user(client)

    data = response.get_json()
    assert "refresh_token" in data["data"]

def test_protected_route_without_token(client):

    response = client.get(
        "/api/v1/users/me"
    )

    assert response.status_code == 401


def test_protected_route_with_valid_token(client, auth_headers):

    response = client.get(
        "/api/v1/users/me",
        headers= auth_headers
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


def test_employee_cannot_access_admin(client):

    register_user(
        client
    )

    login_response = login_user(client)

    token = (
        login_response
        .get_json()["data"]["access_token"]
    )

    response = client.get(
        "/api/v1/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_admin_can_access_admin(client):

    create_user_directly(
        username="admin",
        email="admin@example.com",
        role="Admin"
    )

    login_response = login_user(
        client,
        username="admin"
    )

    token = (
        login_response
        .get_json()["data"]["access_token"]
    )

    response = client.get(
        "/api/v1/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_manager_can_access_management(client):

    create_user_directly(
        username="manager",
        email="manager@example.com",
        role="Manager"
    )

    login_response = login_user(
        client,
        username="manager"
    )

    token = (
        login_response
        .get_json()["data"]["access_token"]
    )

    response = client.get(
        "/api/v1/users/management",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_employee_cannot_access_management(client):

    register_user(client)

    login_response = login_user(client)

    token = (
        login_response
        .get_json()["data"]["access_token"]
    )

    response = client.get(
        "/api/v1/users/management",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_refresh_token(client):

    register_user(client)

    login_response = login_user(client)

    refresh_token = (
        login_response
        .get_json()["data"]["refresh_token"]
    )

    response = client.post(
        "/api/v1/auth/refresh",
        headers={
            "Authorization": f"Bearer {refresh_token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "access_token" in data["data"]

def test_inactive_user_cannot_login(
        client,
        app
):
    register_user(client)

    with app.app_context():
        from app.models.user import User

        user=User.query.filter_by(
            username="testuser"
        ).first()

        user.is_active = False

        db.session.commit()

    response =login_user(client)

    assert response.status_code == 401