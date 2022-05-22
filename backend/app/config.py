import os
from datetime import timedelta


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CRYPTOCOMPARE_API_KEY = "your-api-key"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=30)


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
