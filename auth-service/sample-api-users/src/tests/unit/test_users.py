import json
from datetime import datetime

import pytest
import src.api.users


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def test_add_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_add_user(username, email, passwd):
        d = AttrDict()
        d.update(
            {
                "id": 10,
                "username": "me",
                "email": "me@itba.edu",
                "password": "123456789",
            }
        )
        return d

    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "add_user", mock_add_user)

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@itba.edu",
                "password": "123456789",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "michael@itba.edu was added!" in data["message"]
    assert data["id"] == 10


def test_add_user_duplicate_email(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return True

    def mock_add_user(username, email, passwd):
        d = AttrDict()
        d.update({"id": 1, "username": "me", "email": "me@itba.edu"})
        return d

    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "add_user", mock_add_user)

    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "michael",
                "email": "michael@itba.edu",
                "password": "123456789",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return {
            "id": 1,
            "username": "jeffrey",
            "email": "jeffrey@itba.edu",
            "created_date": datetime.now(),
        }

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/1")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@itba.edu" in data["email"]
    assert "password" not in data


def test_single_user_incorrect_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, monkeypatch):
    def mock_get_all_users():
        return [
            {
                "id": 1,
                "username": "michael",
                "email": "michael@mherman.org",
                "created_date": datetime.now(),
            },
            {
                "id": 1,
                "username": "fletcher",
                "email": "fletcher@notreal.com",
                "created_date": datetime.now(),
            },
        ]

    monkeypatch.setattr(src.api.users, "get_all_users", mock_get_all_users)
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]


def test_remove_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        d = AttrDict()
        d.update(
            {"id": 1, "username": "user-to-be-removed", "email": "remove-me@itba.edu"}
        )
        return d

    def mock_delete_user(user):
        return True

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(src.api.users, "delete_user", mock_delete_user)
    client = test_app.test_client()
    resp_two = client.delete("/users/1")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "remove-me@itba.edu was removed!" in data["message"]


def test_remove_user_incorrect_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        d = AttrDict()
        d.update({"id": 1, "username": "me", "email": "me@itba.edu"})
        return d

    def mock_update_user(user, username, email):
        d = AttrDict()
        d.update({"id": 1, "username": "me", "email": "me@itba.edu"})
        return d

    def mock_get_user_by_email(email):
        return None

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "update_user", mock_update_user)

    client = test_app.test_client()
    resp_one = client.put(
        "/users/1",
        data=json.dumps({"username": "me", "email": "me@itba.edu"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert "1 was updated!" in data["message"]
    resp_two = client.get("/users/1")
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
    test_app, monkeypatch, user_id, payload, status_code, message
):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]


def test_update_user_duplicate_email(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_id(user_id):
        d = AttrDict()
        d.update({"id": 1, "username": "me", "email": "me@itba.edu"})
        return d

    def mock_update_user(user, username, email):
        return True

    def mock_get_user_by_email(email):
        return True

    monkeypatch.setattr(src.api.users, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(src.api.users, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(src.api.users, "update_user", mock_update_user)

    client = test_app.test_client()
    resp = client.put(
        "/users/1",
        data=json.dumps({"username": "me", "email": "me@itba.edu"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]
