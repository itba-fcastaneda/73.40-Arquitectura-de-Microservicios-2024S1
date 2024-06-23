from flask_restx import Api
from src.api.auth import auth_namespace
from src.api.ping import ping_namespace
from src.api.users import NAMESPACE as NAMESPACE_USERS
from src.api.users import users_namespace
from src.api.zones import NAMESPACE as NAMESPACE_ZONES
from src.api.zones import zones_namespace

api = Api(version="1.0", title="Users API", doc="/doc")


api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path=f"/{NAMESPACE_USERS}")
api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(zones_namespace, path=f"/{NAMESPACE_ZONES}")
