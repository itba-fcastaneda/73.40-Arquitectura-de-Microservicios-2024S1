from flask_restx import fields
from sqlalchemy.sql import func
from src import db


class Zone(db.Model):
    __tablename__ = "zones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    create_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_model_full(cls, namespace):
        return namespace.model(
            "ZoneFull",
            {
                "id": fields.Integer(readOnly=True),
                "name": fields.String(required=True),
            },
        )

    @classmethod
    def get_model_create(cls, namespace):
        return namespace.model(
            "ZoneCreate",
            {
                "name": fields.String(required=False),
            },
        )
