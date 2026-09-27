import os
import pytest

from app import create_app, db

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

def test_register_user(client):
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password":"password123"
        }
    )

    assert response.status_code == 201
    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["username"] == "testuser"

def test_duplicate_username(
        client,
        create_user
):
    create_user(
        username= "testuser",
        email= "test@example.com"
    )
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password":"password123" 
        }
    )
    assert response.status_code == 409

def test_duplicate_email(client, create_user):
    create_user(
        username= "testuser",
        email= "test@example.com"
    )
    response = client.post(
        "/api/v1/users/register",
        json = {
            "username": "testuser2",
            "email": "test@example.com",
            "password":"password123"
        }
    )
    assert response.status_code == 409

def test_login_success(client, create_user):

    create_user(
        username= "testuser",
        email= "test@example.com",
        password="password123"
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "username":"testuser",
            "password":"password123"
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True

def test_login_invalid_password(client, create_user):
    create_user(
        username= "testuser",
        email= "test@example.com",
        password="password123"
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "username":"testuser",
            "password":"wrongpassword"
        }
    )
    assert response.status_code == 401

def test_registration_validation(client):
    response = client.post(
        "/api/v1/users/register",
        json = {
            "username": "ab",
            "email": "wrong",
            "password":"123"
        }
    )
    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert "username" in data["errors"]
    assert "email" in data["errors"]
    assert "password" in data["errors"]