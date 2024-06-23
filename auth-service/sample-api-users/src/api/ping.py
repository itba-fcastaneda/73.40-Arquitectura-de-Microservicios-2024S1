from flask import Blueprint
from flask_restx import Api, Namespace, Resource

from src import db
from src.api.models.users import User
from src.api.models.zones import Zone

ping_blueprint = Blueprint("ping", __name__)
api = Api(ping_blueprint)

ping_namespace = Namespace("ping")


class Ping(Resource):
    def delete(self):
        db.drop_all()
        db.create_all()
        db.session.commit()
        return {"status": "recreated"}

    def post(self):
        db.session.add(User(username="fede", email="fede@gmail.com", password="password1234"))
        db.session.add(User(username="martin", email="martin@gmail.com", password="password1234"))
        db.session.add(User(username="nacho", email="nacho@gmail.com", password="password1234"))
        db.session.add(Zone(name="Belgrano"))
        db.session.add(Zone(name="San Isidro"))
        db.session.commit()
        return {"status": "seeded"}

    def get(self):
        return {"status": "success", "message": "pong!"}


ping_namespace.add_resource(Ping, "")
