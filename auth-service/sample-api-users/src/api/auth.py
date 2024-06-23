import jwt
from flask import request
from flask_restx import Namespace, Resource
from src import bcrypt
from src.api.cruds.users import add_user, get_user_by_email, get_user_by_id
from src.api.models.users import User

auth_namespace = Namespace("auth")

auth_user_model = User.get_api_auth_user_model(auth_namespace)
auth_full_user_model = User.get_api_auth_full_user_model(auth_namespace)
auth_login_model = User.get_api_auth_login_model(auth_namespace)
auth_refresh_model = User.get_api_auth_refresh_model(auth_namespace)
auth_tokens_model = User.get_api_auth_tokens_model(auth_namespace)

parser = auth_namespace.parser()
parser.add_argument("Authorization", location="headers")


class Register(Resource):
    @auth_namespace.marshal_with(auth_user_model)
    @auth_namespace.expect(auth_full_user_model, validate=True)
    @auth_namespace.response(201, "Success")
    @auth_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")

        user = get_user_by_email(email)
        if user:
            auth_namespace.abort(400, "Sorry. That email already exists.")
        user = add_user(username, email, password)

        return user, 201


class Login(Resource):
    @auth_namespace.marshal_with(auth_tokens_model)
    @auth_namespace.expect(auth_login_model, validate=True)
    @auth_namespace.response(201, "Success")
    @auth_namespace.response(404, "User does not exist")
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            auth_namespace.abort(404, "User does not exist")

        access_token = user.encode_token(user.id, "access")
        refresh_token = user.encode_token(user.id, "refresh")

        response_object = {"access_token": access_token, "refresh_token": refresh_token}
        return response_object, 200


class Refresh(Resource):
    @auth_namespace.marshal_with(auth_tokens_model)
    @auth_namespace.expect(auth_refresh_model, validate=True)
    @auth_namespace.response(200, "Success")
    @auth_namespace.response(401, "Invalid token")
    def post(self):
        post_data = request.get_json()
        refresh_token = post_data.get("refresh_token")
        response_object = {}

        try:
            user_id = User.decode_token(refresh_token)
            user = get_user_by_id(user_id)

            if not user:
                auth_namespace.abort(401, "Invalid token")

            access_token = user.encode_token(user.id, "access")
            refresh_token = user.encode_token(user.id, "refresh")

            response_object = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return response_object, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Signature expired. Please log in again.")
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")


class Status(Resource):
    @auth_namespace.marshal_with(auth_user_model)
    @auth_namespace.response(200, "Success")
    @auth_namespace.response(401, "Invalid token")
    @auth_namespace.expect(parser)
    def get(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_header_list = auth_header.split(" ")
                if len(auth_header_list) != 2:
                    raise jwt.InvalidTokenError(f"Invalid header: {auth_header}")
                access_token = auth_header_list[1]
                resp = User.decode_token(access_token)
                user = get_user_by_id(resp)
                if not user:
                    auth_namespace.abort(401, "Invalid token")
                return user, 200
            except jwt.ExpiredSignatureError:
                auth_namespace.abort(401, "Signature expired. Please log in again.")
                return "Signature expired. Please log in again."
            except jwt.InvalidTokenError:
                auth_namespace.abort(401, "Invalid token. Please log in again.")
        else:
            auth_namespace.abort(403, "Token required")


auth_namespace.add_resource(Register, "/register")
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Refresh, "/refresh")
auth_namespace.add_resource(Status, "/status")
