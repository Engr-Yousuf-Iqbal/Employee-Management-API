import os
import pytest
from app import create_app, db

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

def test_login_creates_audit_log(
    client,
    create_user
):

    from app.models.audit_log import AuditLog

    user = create_user(
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

    assert response.status_code == 200

    log = AuditLog.query.filter_by(
        user_id=user.id,
        action="LOGIN"
    ).first()

    assert log is not None
    assert log.resource == "USER"