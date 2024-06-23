import json

import pytest
from src.api.cruds.zones import add_zone, get_zone_by_id
from src.api.zones import NAMESPACE as ZONE_NAMESPACE

ZONE_NAME = "San Isidro"
ZONE_NAME_2 = "Bajo San Isidro"
ZONE_INVALID_ID = 99999999


def test_zone_add(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        f"/{ZONE_NAMESPACE}",
        data=json.dumps({"name": "Belgrano"}),
        content_type="application/json",
    )

    assert resp.status_code == 201
    data = json.loads(resp.data.decode())
    assert "Belgrano was added!" in data["message"]
    assert "id" in data
    assert isinstance(data["id"], int)


INVALID_ADD_PAYLOADS = [{}, {"name": ""}, {"names": "bla bla"}]


@pytest.mark.parametrize("payload", INVALID_ADD_PAYLOADS)
def test_zone_add_no_desc(test_app, test_database, payload):
    client = test_app.test_client()
    resp = client.post(
        f"/{ZONE_NAMESPACE}",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert "Invalid payload" in data["message"]


def test_zone_get_all(test_app, test_database):
    client = test_app.test_client()
    add_zone(ZONE_NAME)
    resp = client.get(f"/{ZONE_NAMESPACE}")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert isinstance(data, list)
    assert len(data) > 0


def test_zone_get(test_app, test_database):
    client = test_app.test_client()
    zone = add_zone(ZONE_NAME)
    resp = client.get(f"/{ZONE_NAMESPACE}/{zone.id}")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == zone.id
    assert "name" in data
    assert data["name"] == ZONE_NAME


def test_zone_get_not_found(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(f"/{ZONE_NAMESPACE}/{ZONE_INVALID_ID}")
    assert resp.status_code == 404
    data = json.loads(resp.data.decode())
    assert "message" in data
    assert f"Zone {ZONE_INVALID_ID} does not exist" in data["message"]


def test_zone_update(test_app, test_database):
    client = test_app.test_client()
    zone = add_zone(ZONE_NAME)
    body = {"name": ZONE_NAME_2}
    resp = client.put(f"/{ZONE_NAMESPACE}/{zone.id}", json=body)
    assert resp.status_code == 200
    updated_zone = get_zone_by_id(zone.id)
    assert updated_zone.name == ZONE_NAME_2


def test_zone_update_not_found(test_app, test_database):
    client = test_app.test_client()
    body = {"name": ZONE_NAME_2}
    resp = client.put(f"/{ZONE_NAMESPACE}/{ZONE_INVALID_ID}", json=body)
    assert resp.status_code == 404
    data = json.loads(resp.data.decode())
    assert "message" in data
    assert f"Zone {ZONE_INVALID_ID} does not exist" in data["message"]


@pytest.mark.parametrize("payload", INVALID_ADD_PAYLOADS)
def test_zone_update_invalid_payload(test_app, test_database, payload):
    client = test_app.test_client()
    zone = add_zone(ZONE_NAME)
    resp = client.put(f"/{ZONE_NAMESPACE}/{zone.id}", json=payload)

    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert "Invalid payload" in data["message"]


def test_zone_delete(test_app, test_database):
    client = test_app.test_client()
    zone = add_zone(ZONE_NAME)
    zone_id = zone.id
    resp = client.delete(f"/{ZONE_NAMESPACE}/{zone_id}")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert "message" in data
    assert data["message"] == "Success"
    zone = get_zone_by_id(zone_id)
    assert not zone


def test_zone_delete_not_found(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete(f"/{ZONE_NAMESPACE}/{ZONE_INVALID_ID}")
    assert resp.status_code == 404
    data = json.loads(resp.data.decode())
    assert "message" in data
    assert f"Zone {ZONE_INVALID_ID} does not exist" in data["message"]
