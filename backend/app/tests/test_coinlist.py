import json

import pytest
from flask import current_app
'''

def test_portfolio(test_app, test_database, add_trade, add_user):
    client = test_app.test_client()
    user_id = 1
    exchange = "ex"
    user = add_user("test", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "1", 1, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "2", 2, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE2", "QUOTE", "3", 3, "buy", 1, 1)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "test", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/QUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 2

def test_portfolio_fifo(test_app, test_database, add_trade, add_user):
    client = test_app.test_client()
    exchange = "ex"
    user = add_user("test2", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "10", 10, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "20", 20, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "30", 60, "sell", 2, .5)
    add_trade(user.id, exchange, "BASE", "QUOTE", "40", 70, "sell", 2, 1)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "test2", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/QUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 1
    assert data[0]["realized_amount"] == 1.5



def test_portfolio_fifo2(test_app, test_database, add_trade, add_user):
    client = test_app.test_client()
    exchange = "ex"
    user = add_user("ftest2", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "11", 10, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "41", 70, "sell", 1, 1)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "ftest2", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/QUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 1
    assert data[0]["realized_amount"] == 1

def test_portfolio_fifo2(test_app, test_database, add_trade, add_user):
    client = test_app.test_client()
    exchange = "ex"
    user = add_user("ftest3", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "12", 10, "buy", 2, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "22", 11, "buy", 2, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "32", 12, "buy", 2, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "42", 13, "buy", 2, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "52", 74, "sell", 4, 3.2)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "ftest3", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/QUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 1
    assert data[0]["realized_amount"] == 3.2

def test_portfolio_normalize_quote(test_app, test_database, add_trade, add_user, add_daily_price):
    client = test_app.test_client()
    exchange = "ex"
    day_seconds = 86400
    user = add_user("test3", "test")
    add_daily_price("QUOTE2/QUOTE", 0, .5, .5, .5, .5, exchange)
    add_daily_price("QUOTE/QUOTE2", day_seconds, 3, 3, 3, 3, exchange)
    add_trade(user.id, exchange, "BASE", "QUOTE", "100", 10, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE2", "200", 20, "buy", 2, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE2", "300", (day_seconds* 1000) + 10, "buy", 3, 1)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "test3", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/QUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 1
    assert data[0]["cost"] == 3

def test_portfolio_normalize_quote2(test_app, test_database, add_trade, add_user, add_daily_price):
    client = test_app.test_client()
    exchange = "ex"
    day_seconds = 86400
    user = add_user("test4", "test")
    add_daily_price("BTC/BQUOTE", 0, .1, .1, .1, .1, exchange)
    add_daily_price("BTC/BQUOTE2", 0, .2, .2, .2, .2, exchange)
    add_trade(user.id, exchange, "BBASE", "BQUOTE", "1000", 10, "buy", 1, 1)
    add_trade(user.id, exchange, "BBASE", "BQUOTE2", "2000", 20, "buy", 2, 1)

    resp = client.post(
        "/user/login",
        data=json.dumps({"username": "test4", "password": "test"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    resp = client.get(
        "/coinlist/portfolio/BQUOTE",
        headers={"Authorization": "Bearer {}".format(data["access_token"])},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert resp.content_type == "application/json"
    assert len(data) == 1
    assert data[0]["cost"] == 2

'''