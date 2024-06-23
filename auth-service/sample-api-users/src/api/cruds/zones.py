from src import db
from src.api.models.zones import Zone


def get_all_zones():
    return Zone.query.all()


def get_zone_by_id(zone_id):
    return Zone.query.filter_by(id=zone_id).first()


def add_zone(name):
    zone = Zone(name=name)
    db.session.add(zone)
    db.session.commit()
    return zone


def update_zone(zone, name):
    zone.name = name
    db.session.commit()
    return zone


def delete_zone(zone):
    db.session.delete(zone)
    db.session.commit()
    return zone
