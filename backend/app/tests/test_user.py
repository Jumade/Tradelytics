# services/users/app/tests/test_auth.py

from datetime import timedelta

import json

import pytest
from flask import current_app


def test_user_registration(test_app, test_database, add_user):
    client = test_app.test_client()
    resp = client.post(
        "/user/register",
        data=json.dumps(
            {
                "username": "justatest",
                "password": "123456",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert "justatest" in data["username"]
    assert "password" not in data


def test_user_registration_duplicate_username(test_app, test_database, add_user):
    add_user("michael", "test")
    client = test_app.test_client()
    resp = client.post(
        "/user/register",
        data=json.dumps(
            {"username": "michael", "password": "test"}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert resp.content_type == "application/json"
    assert "Sorry. That email already exists." in data["message"]



def test_registered_user_login(test_app, test_database, add_user):
    add_user("test3", "test")
    client = test_app.test_client()
    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "test3", "password": "test"}),
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
        "/user/login",
        data=json.dumps({"username": "testnotreal", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert resp.content_type == "application/json"
    assert "User does not exist." in data["message"]


def test_valid_refresh(test_app, test_database, add_user):
    add_user("test4", "test")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/user/login",
        data=json.dumps({"username": "test4", "password": "test"}),
        content_type="application/json",
    )
    # valid refresh
    data = json.loads(resp_login.data.decode())
    refresh_token = json.loads(resp_login.data.decode())["refresh_token"]
    resp = client.get(
        "/user/refresh",
        headers={"Authorization": "Bearer {}".format(refresh_token)},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_invalid_refresh(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        "/user/refresh",
        headers={"Authorization": "Bearer {}".format("test")},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code != 200
    assert resp.content_type == "application/json"



def test_get_settings(test_app, test_database, add_user, add_exchange):
    user = add_user("exchanges_test", "test")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/user/login",
        data=json.dumps({"username": "exchanges_test", "password": "test"}),
        content_type="application/json",
    )

    token = json.loads(resp_login.data.decode())["access_token"]
    add_exchange(user.id, "ex_name", "exchange_id", "test_key", "test_secret", True)
    resp = client.get(
        "/user/settings",
        headers={"Authorization": "Bearer {}".format(token)},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert data["name"] == "exchanges_test"
    assert len(data["exchanges"]) == 1

def test_add_exchanges(test_app, test_database, add_user, add_exchange):
    user = add_user("exchanges_test2", "test")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/user/login",
        data=json.dumps({"username": "exchanges_test2", "password": "test"}),
        content_type="application/json",
    )

    token = json.loads(resp_login.data.decode())["access_token"]

    resp = client.post(
        "/user/exchange",
        data=json.dumps({"name": "testname", "apikey": "testapikey",  "apisecret": "testapisecret", "exchange_id":"testexchange"}),
        headers={"Authorization": "Bearer {}".format(token)},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert len(data["exchanges"]) == 1



def test_update_exchanges(test_app, test_database, add_user, add_exchange):
    user = add_user("exchanges_test3", "test")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/user/login",
        data=json.dumps({"username": "exchanges_test3", "password": "test"}),
        content_type="application/json",
    )

    token = json.loads(resp_login.data.decode())["access_token"]
    exchange = add_exchange(user.id, "ex_name", "exchange_id", "test_key", "test_secret", True)
    resp = client.put(
        "/user/exchange-update/{}".format(exchange.id),
        data=json.dumps({"name": "testname", "apikey": "testapikey32",  "apisecret": "testapisecret", "exchange_id":"testexchange"}),
        headers={"Authorization": "Bearer {}".format(token)},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert len(data["exchanges"]) == 1
    assert data["exchanges"][0]["name"] == "testname"
    assert data["exchanges"][0]["apikey"] == "testapikey32"

