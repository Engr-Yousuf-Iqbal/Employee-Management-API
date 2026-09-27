import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(
            os.getenv(
                "JWT_ACCESS_TOKEN_EXPIRES",
                900
            )
        )
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(
            os.getenv(
                "JWT_ACCESS_TOKEN_EXPIRES",
                2592000
            )
        )
    )


    BCRYPT_LOG_ROUNDS = int(
        os.getenv("BCRYPT_LOG_ROUNDS",12)
    )

class DevelopmentConfig(Config):

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):

    DEBUG = False
    TESTING = False