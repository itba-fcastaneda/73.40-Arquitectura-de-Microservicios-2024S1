from flask import request
from flask_restx import Namespace, Resource
from src.api.models.users import User

from src.api.cruds.users import (  # isort:skip
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)

NAMESPACE = "users"

users_namespace = Namespace(NAMESPACE)

user_api_model = User.get_api_user_model(users_namespace)
user_post_api_model = User.get_api_user_post_model(users_namespace)


class UsersList(Resource):
    @users_namespace.response(200, "Success")
    @users_namespace.marshal_with(user_api_model, as_list=True)
    def get(self):
        return get_all_users(), 200

    @users_namespace.response(201, "<user_email> was added!")
    @users_namespace.response(400, "Sorry. That email already exists.")
    @users_namespace.expect(user_post_api_model, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        user = add_user(username, email, password)

        response_object["message"] = f"{email} was added!"
        response_object["id"] = user.id
        return response_object, 201


class Users(Resource):
    @users_namespace.response(200, "Success")
    @users_namespace.response(404, "User <user_id> does not exist")
    @users_namespace.marshal_with(user_api_model)
    def get(self, user_id):
        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.response(200, "<user_id> was updated!")
    @users_namespace.response(404, "User <user_id> does not exist")
    @users_namespace.response(400, "Sorry. That email already exists.")
    @users_namespace.expect(user_api_model, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)  # updated
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):  # updated
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        user = update_user(user, username, email)  # new

        response_object["message"] = f"{user.id} was updated!"
        response_object["id"] = user.id
        return response_object, 200

    @users_namespace.response(200, "<user_id> was removed!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(self, user_id):
        response_object = {}
        user = get_user_by_id(user_id)

        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")

        delete_user(user)

        response_object["message"] = f"{user.email} was removed!"
        response_object["id"] = user.id
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")
