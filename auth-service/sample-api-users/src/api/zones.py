from flask import request
from flask_restx import Namespace, Resource
from src.api.models.generic import get_model_create_response
from src.api.models.zones import Zone as ZoneModel

from src.api.cruds.zones import (  # isort:skip
    get_all_zones,
    get_zone_by_id,
    add_zone,
    update_zone,
    delete_zone,
)

NAMESPACE = "zones"

zones_namespace = Namespace(NAMESPACE)

zone_model_full = ZoneModel.get_model_full(namespace=zones_namespace)
zone_model_create = ZoneModel.get_model_create(namespace=zones_namespace)
zone_model_create_response = get_model_create_response(namespace=zones_namespace)


class ZonesList(Resource):
    @zones_namespace.response(201, "Zone was added!")
    @zones_namespace.response(400, "Invalid payload")
    @zones_namespace.expect(zone_model_create, validate=True)
    @zones_namespace.marshal_with(zone_model_create_response)
    def post(self):
        post_data = request.get_json()
        name = post_data.get("name")
        response_object = {}

        if not name:
            response_object["message"] = "Invalid payload"
            return response_object, 400

        zone = add_zone(name=name)

        response_object["message"] = f"{name} was added!"
        response_object["id"] = zone.id
        return response_object, 201

    @zones_namespace.response(200, "Success")
    @zones_namespace.marshal_with(zone_model_full, as_list=True)
    def get(self):
        return get_all_zones(), 200


class Zones(Resource):
    @zones_namespace.response(200, "Success")
    @zones_namespace.response(404, "Zone <zone_id> does not exist")
    @zones_namespace.marshal_with(zone_model_full)
    def get(self, zone_id):
        zone = get_zone_by_id(zone_id)
        if not zone:
            zones_namespace.abort(404, f"Zone {zone_id} does not exist")
        return zone, 200

    @zones_namespace.response(200, "<zone_id> was updated!")
    @zones_namespace.response(404, "Zone <zone_id> does not exist")
    @zones_namespace.response(400, "Invalid payload.")
    @zones_namespace.expect(zone_model_create, validate=True)
    def put(self, zone_id):
        post_data = request.get_json()
        name = post_data.get("name")
        response_object = {}

        if not name:
            zones_namespace.abort(400, "Invalid payload.")

        zone = get_zone_by_id(zone_id)
        if not zone:
            zones_namespace.abort(404, f"Zone {zone_id} does not exist")

        zone = update_zone(zone, name)

        response_object["message"] = f"{zone.id} was updated!"
        response_object["id"] = zone.id
        return response_object, 200

    @zones_namespace.response(200, "Success")
    @zones_namespace.response(404, "Zone <zone_id> does not exist")
    def delete(self, zone_id):
        response_object = {}

        zone = get_zone_by_id(zone_id)
        if not zone:
            zones_namespace.abort(404, f"Zone {zone_id} does not exist")

        delete_zone(zone)

        response_object["message"] = "Success"
        return response_object, 200


zones_namespace.add_resource(ZonesList, "")
zones_namespace.add_resource(Zones, "/<int:zone_id>")
