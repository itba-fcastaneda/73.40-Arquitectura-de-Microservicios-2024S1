import json

import pytest
from src import bcrypt
from src.api.cruds.users import get_user_by_id
from src.api.models.users import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "fede",
                "email": "fcastaneda@itba.edu.ar",
                "password": "1234566789",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "fcastaneda@itba.edu.ar was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@begood.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "fede", "email": "fcastaneda@itba.edu.ar"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "federico",
                "email": "fcastaneda@itba.edu.ar",
                "password": "passwd1234",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("fede", "fede@itba.edu", "passwd1234")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "fede" in data["username"]
    assert "fede@itba.edu" in data["email"]
    assert "password" not in data  # Password must not be returned


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("martin", "martin@itba.edu", "passwd1234")
    add_user("nacho", "nacho@itba.edu", "passwd1234")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "martin" in data[0]["username"]
    assert "martin@itba.edu" in data[0]["email"]
    assert "nacho" in data[1]["username"]
    assert "nacho@itba.edu" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]


def test_remove_user(test_app, test_database, add_user):
    USER_EMAIL = "remove-me@itba.edu"
    test_database.session.query(User).delete()
    user = add_user("user-to-be-removed", USER_EMAIL, "passwd1234")
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert f"{USER_EMAIL} was removed!" in data["message"]

    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user(test_app, test_database, add_user):
    user = add_user("user-to-be-updated", "update-me@itba.edu", "passwd1234")
    client = test_app.test_client()
    resp_one = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "me", "email": "me@itba.edu"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{user.id} was updated!" in data["message"]

    resp_two = client.get(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "me" in data["username"]
    assert "me@itba.edu" in data["email"]


@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"email": "me@itba.edu"}, 400, "Input payload validation failed"],
        [
            999,
            {"username": "me", "email": "me@itba.edu"},
            404,
            "User 999 does not exist",
        ],
    ],
)
def test_update_user_invalid(
    test_app, test_database, user_id, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_update_user_duplicate_email(test_app, test_database, add_user):
    add_user("carlos", "carlos@garca.org", "passwd1234")
    user = add_user("charly", "charly@garca.org", "passwd1234")

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "charly", "email": "carlos@garca.org"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_update_user_with_passord(test_app, test_database, add_user):
    password_one = "greaterthaneight"
    password_two = "somethingdifferent"

    user = add_user("user-to-be-updated", "update-me@testdriven.io", password_one)
    assert bcrypt.check_password_hash(user.password, password_one)

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {"username": "me", "email": "foo@testdriven.io", "password": password_two}
        ),
        content_type="application/json",
    )
    assert resp.status_code == 200

    user = get_user_by_id(user.id)
    assert bcrypt.check_password_hash(user.password, password_one)
    assert not bcrypt.check_password_hash(user.password, password_two)
