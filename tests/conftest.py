import os
import pytest

from app import create_app, db


@pytest.fixture
def app():

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DB_URI"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key"
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
def create_user(app):

    from app.models.user import User
    from app.utils.password import hash_password

    def _create_user(
        username="testuser",
        email="test@example.com",
        password="password123",
        role="Employee"
    ):
        hash=hash_password(password)
        user = User(
            username=username,
            email=email,
            role=role,
            password_hash = hash
        )

        db.session.add(user)
        db.session.commit()

        return user

    return _create_user

@pytest.fixture
def auth_headers(client, create_user):

    create_user(
        username="john",
        email="john@example.com",
        password="password123"
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "username": "john",
            "password": "password123"
        }
    )

    token = (
        response
        .get_json()["data"]["access_token"]
    )

    return {
        "Authorization": f"Bearer {token}"
    }

