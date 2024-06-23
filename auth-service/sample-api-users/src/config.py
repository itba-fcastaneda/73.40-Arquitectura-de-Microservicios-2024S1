import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 5
    REFRESH_TOKEN_EXPIRATION = 5


class ProductionConfig(BaseConfig):
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")

    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
        url = os.environ.get("DATABASE_URL")
        if url is not None and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        self.SQLALCHEMY_DATABASE_URI = url
