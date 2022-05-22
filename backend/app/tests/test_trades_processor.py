import json

import pytest
from flask import current_app
from app.api.db_models.positions import Position
from app.api.db_models.daily_price import DailyPrice
from app.background.trades_processor import process_trades


def test_processing_smaller_trade(test_app, test_database, add_trade, add_user):
    exchange = "ex"
    user = add_user("test", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "1", 1, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "2", 2, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "3", 3, "sell", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "4", 4, "sell", .5, .5)

    process_trades(user.id)
    
    positions = test_database.session.query(Position).filter_by(user_id=user.id).all()
   
    assert len(positions) == 3
    assert positions[0].open_price == 1
    assert positions[0].close_price == 1
    assert positions[1].open_price == 1
    assert positions[1].close_price == .5
    assert positions[1].size == .5

def test_processing_bigger_trade(test_app, test_database, add_trade, add_user):
    exchange = "ex"
    Position.query.delete()
    test_database.session.commit()

    user = add_user("test2", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "11", 1, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "12", 2, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "13", 3, "sell", 1.5, 1.5)
    
    process_trades(user.id)
    
    query = test_database.session.query(Position).filter_by(user_id=user.id)
    positions = query.all()
   
    assert len(positions) == 3
    assert positions[0].open_price == 1
    assert positions[0].close_price == 1.5
    assert positions[1].open_price == 1
    assert positions[1].close_price == 1.5
    assert positions[1].size == .5

    assert positions[2].open_price == 1
    assert positions[2].size == .5

def test_processing_bigger_trade_time(test_app, test_database, add_trade, add_user):
    exchange = "ex"
    Position.query.delete()
    test_database.session.commit()

    user = add_user("test3", "test")
    add_trade(user.id, exchange, "BASE", "QUOTE", "21", 1, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "22", 2, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "23", 3, "buy", 1, 1)
    add_trade(user.id, exchange, "BASE", "QUOTE", "24", 4, "sell", 1.5, 1.5)
    
    process_trades(user.id)
    
    query = test_database.session.query(Position).filter_by(user_id=user.id).order_by(Position.open_timestamp.asc(), Position.split_count.asc())
    positions = query.all()
   
    assert len(positions) == 4
    assert positions[0].open_price == 1
    assert positions[0].close_price == 1.5
    assert positions[0].open_timestamp == 1
    assert positions[1].open_price == 1
    assert positions[1].close_price == 1.5
    assert positions[1].size == .5
    assert positions[1].open_timestamp == 2

    assert positions[2].open_price == 1
    assert positions[2].size == .5
    assert positions[2].open_timestamp == 2

    assert positions[3].open_timestamp == 3



def test_processing_normalize_quote(test_app, test_database, add_trade, add_user, add_daily_price):
    exchange = "ex"
    Position.query.delete()
    test_database.session.commit()

    day_seconds = 86400
    user = add_user("test4", "test")
    add_daily_price("QUOTE/BTC", 0, .5, .5, .5, .5, exchange)
    add_daily_price("QUOTE/USD", 0, 2, 2, 2, 2, exchange)
    add_daily_price("QUOTE/EUR", 0, 5, 5, 5, 5, exchange)
    add_trade(user.id, exchange, "BASE", "QUOTE", "100", 10, "buy", 1, 1)

    process_trades(user.id)
    
    query = test_database.session.query(Position).filter_by(user_id=user.id).order_by(Position.open_timestamp.asc(), Position.split_count.asc())
    positions = query.all()

    assert len(positions) == 1
    assert positions[0].open_price == 1
    assert positions[0].open_price_btc == .5
    assert positions[0].open_price_usd == 2
    assert positions[0].open_price_eur == 5

def test_processing_normalize_quote_reverse(test_app, test_database, add_trade, add_user, add_daily_price):
    exchange = "ex"
    Position.query.delete()
    DailyPrice.query.delete()
    test_database.session.commit()

    day_seconds = 86400
    user = add_user("test5", "test")
    add_daily_price("BTC/QUOTE", 0, 2, 2, 2, 2, exchange)
    add_daily_price("USD/QUOTE", 0, .5, .5, .5, .5, exchange)
    add_daily_price("EUR/QUOTE", 0, 1/5, 1/5, 1/5, 1/5, exchange)
    add_trade(user.id, exchange, "BASE", "QUOTE", "101", 10, "buy", 1, 1)

    process_trades(user.id)
    
    query = test_database.session.query(Position).filter_by(user_id=user.id).order_by(Position.open_timestamp.asc(), Position.split_count.asc())
    positions = query.all()

    assert len(positions) == 1
    assert positions[0].open_price == 1
    assert positions[0].open_price_btc == .5
    assert positions[0].open_price_usd == 2
    assert positions[0].open_price_eur == 5

def test_processing_normalize_quote_btc_triangle(test_app, test_database, add_trade, add_user, add_daily_price):
    exchange = "ex"
    Position.query.delete()
    DailyPrice.query.delete()
    test_database.session.commit()

    day_seconds = 86400
    user = add_user("test6", "test")
    add_daily_price("QUOTE/BTC", 0, .5, .5, .5, .5, exchange)
    add_daily_price("BTC/USD", 0, 4, 4, 4, 4, exchange)
    add_daily_price("BTC/EUR", 0, 10, 10, 10, 10, exchange)

    add_trade(user.id, exchange, "BASE", "QUOTE", "102", 10, "buy", 1, 1)

    process_trades(user.id)
    
    query = test_database.session.query(Position).filter_by(user_id=user.id).order_by(Position.open_timestamp.asc(), Position.split_count.asc())
    positions = query.all()

    assert len(positions) == 1
    assert positions[0].open_price == 1
    assert positions[0].open_price_btc == .5
    assert positions[0].open_price_usd == 2
    assert positions[0].open_price_eur == 5
    
    
