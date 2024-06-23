import json
import time

import pytest

TEST_USERNAME = "fede_auth"
TEST_EMAIL = "fede_auth@gmail.com"
TEST_PASSWD = "password1234"


def test_user_registration(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": TEST_USERNAME,
                "email": TEST_EMAIL,
                "password": TEST_PASSWD,
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert TEST_USERNAME in data["username"]
    assert TEST_EMAIL in data["email"]
    assert "password" not in data


def test_user_registration_duplicate_email(test_app, test_database, add_user):
    add_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWD)
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {"username": "martin", "email": TEST_EMAIL, "password": "test"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Sorry. That email already exists." == data["message"]


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"email": TEST_EMAIL, "password": TEST_PASSWD},
        {"username": TEST_USERNAME, "password": TEST_PASSWD},
        {"email": TEST_EMAIL, "username": TEST_USERNAME},
        {"mail": TEST_EMAIL, "username": TEST_USERNAME, "password": TEST_PASSWD},
        {"email": TEST_EMAIL, "user": TEST_USERNAME, "password": TEST_PASSWD},
        {"email": TEST_EMAIL, "username": TEST_USERNAME, "passwd": TEST_PASSWD},
    ],
)
def test_user_registration_invalid_json(test_app, test_database, payload):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Input payload validation failed" in data["message"]


def test_registered_user_login(test_app, test_database, add_user):
    add_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWD)
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": TEST_EMAIL, "password": TEST_PASSWD}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_not_registered_user_login(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps({"email": "invalid@gmail.com", "password": TEST_PASSWD}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert resp.content_type == "application/json"
    assert "User does not exist." in data["message"]


def test_valid_refresh(test_app, test_database, add_user):
    add_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWD)
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": TEST_EMAIL, "password": TEST_PASSWD}),
        content_type="application/json",
    )
    # valid refresh
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert data["access_token"]
    assert data["refresh_token"]
    assert resp.content_type == "application/json"


def test_invalid_refresh_expired_token(test_app, test_database, add_user):
    add_user("test5", "test5@test.com", "test")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test5@test.com", "password": "test"}),
        content_type="application/json",
    )
    # invalid token refresh
    time.sleep(10)
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Signature expired. Please log in again." in data["message"]


def test_invalid_refresh(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "Invalid"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Invalid token. Please log in again." in data["message"]


def test_user_status(test_app, test_database, add_user):
    add_user("test6", "test6@test.com", "test")
    client = test_app.test_client()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps({"email": "test6@test.com", "password": "test"}),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["access_token"]
    resp = client.get(
        "/auth/status",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert "test6" in data["username"]
    assert "test6@test.com" in data["email"]
    assert "password" not in data


def test_invalid_status(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        "/auth/status",
        headers={"Authorization": "Bearer invalid"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert resp.content_type == "application/json"
    assert "Invalid token. Please log in again." in data["message"]
