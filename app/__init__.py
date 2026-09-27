import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.middleware.error_handler import register_error_handlers
from flask_migrate import Migrate

jwt = JWTManager()

migrate = Migrate()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        "200 per day",
        "50 per hour"
    ]
)

def create_app(test_config=None):

    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    else:
        envirnment = os.getenv(
            "FLASK_ENV",
            "development"
        )

        if envirnment == "production":
            app.config.from_object(
                "app.config.settings.ProductionConfig"
            )
        else:
            app.config.from_object(
                "app.config.settings.DevelopmentConfig"
            )
    

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    Swagger(app)

    limiter.init_app(app)

    # Register user routes
    from app.routes.user_routes import user_bp

    app.register_blueprint(user_bp,url_prefix="/api/v1/users")

    # Register Auth routes
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp,url_prefix="/api/v1/auth")

    # Employee routes

    from app.routes.employee_routes import employee_bp

    app.register_blueprint(
        employee_bp,
        url_prefix="/api/v1/employees"
    )

    from app.routes.audit_routes import audit_bp

    app.register_blueprint(
        audit_bp,
        url_prefix="/api/v1/audit"
    )
    
    # Register error handlers
    register_error_handlers(app,jwt)

    return app
    