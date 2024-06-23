import os

from src.config import ProductionConfig


def test_development_config(test_app):
    test_app.config.from_object("src.config.DevelopmentConfig")
    assert test_app.config["SECRET_KEY"] == "my_precious"
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000


def test_testing_config(test_app):
    test_app.config.from_object("src.config.TestingConfig")
    assert test_app.config["SECRET_KEY"] == "my_precious"
    assert test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 5
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 5


def test_production_config(test_app, monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://postgres:postgres@api-db:5432/api_users"
    )
    test_app.config.from_object(ProductionConfig())
    # assert test_app.config["SECRET_KEY"] == "my_precious"
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 13
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000


def test_production_db_url_rewrite(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://server")
    prod_config = ProductionConfig()
    assert prod_config.SQLALCHEMY_DATABASE_URI == "postgresql://server"
