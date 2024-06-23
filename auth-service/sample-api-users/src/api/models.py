import datetime

import jwt
from flask import current_app
from flask_restx import fields
from sqlalchemy.sql import func
from src import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()

    @staticmethod
    def encode_token(user_id, token_type):
        print(f"encode_token(user_id={user_id}, token_type={token_type}):")
        if token_type == "access":
            seconds = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
        else:
            seconds = current_app.config.get("REFRESH_TOKEN_EXPIRATION")

        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )

    @staticmethod
    def decode_token(token):
        decoded = jwt.decode(
            token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
        )
        return decoded["sub"]

    @classmethod
    def get_api_user_model(cls, namespace):
        return namespace.model(
            "User",
            {
                "id": fields.Integer(readOnly=True),
                "username": fields.String(required=True),
                "email": fields.String(required=True),
                "created_date": fields.DateTime,
            },
        )

    @classmethod
    def get_api_user_post_model(cls, namespace):
        return namespace.inherit(
            "User Post",
            cls.get_api_user_model(namespace),
            {
                "password": fields.String(required=False),
            },
        )

    @classmethod
    def get_api_auth_user_model(cls, namespace):
        return namespace.model(
            "User",
            {
                "username": fields.String(required=True),
                "email": fields.String(required=True),
            },
        )

    @classmethod
    def get_api_auth_full_user_model(cls, namespace):
        return namespace.clone(
            "User Full",
            cls.get_api_auth_user_model(namespace),
            {
                "password": fields.String(required=True),
            },
        )

    @classmethod
    def get_api_auth_login_model(cls, namespace):
        return namespace.model(
            "User",
            {
                "password": fields.String(required=True),
                "email": fields.String(required=True),
            },
        )

    @classmethod
    def get_api_auth_refresh_model(cls, namespace):
        return namespace.model(
            "Refresh", {"refresh_token": fields.String(required=True)}
        )

    @classmethod
    def get_api_auth_tokens_model(cls, namespace):
        return namespace.clone(
            "Access and Refresh Token",
            cls.get_api_auth_refresh_model(namespace),
            {"access_token": fields.String(required=True)},
        )
