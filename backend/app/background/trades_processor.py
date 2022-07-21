
import time
import os
import sys
from app import db
from app.api.db_models.trades import Trade
from app.api.db_models.positions import Position
from app.api.db_models.daily_price import DailyPrice
from app.api.db_models.user import User

import datetime 


import ccxt  
from app.api.db_models.exchange import Exchange
def process_all_trades():
    users = User.query.all()
    for user in users:
        process_trades(user.id)

def process_trades(user_id):
    query = Trade.query.filter_by(processed=False, user_id=user_id).order_by(Trade.timestamp.asc())
    trades = query.all()
    for trade in trades:
        if trade.side == "buy":
            open_position(trade)
        elif trade.side == "sell":
            close_position(trade.baseAsset, trade.amount, trade.price, trade.timestamp)
        trade.processed = True
    db.session.commit()

def open_position(trade):
    position = Position(trade.user_id, trade.baseAsset, trade.quoteAsset, trade.amount, trade.timestamp, trade.price)
    add_open_quote_prices(position)
    db.session.add(position)
    db.session.commit()


def close_position(baseAsset, amount, price, timestamp):
    next_open_position = Position.query.filter_by(baseAsset=baseAsset, closed=False).order_by(Position.open_timestamp.asc(), Position.split_count.asc()).first()
    if next_open_position == None:
        return
    if next_open_position.size == amount:
        next_open_position.closed = True
        next_open_position.close_price = price
        add_close_quote_prices(next_open_position, timestamp)
    elif next_open_position.size > amount:
        size_diff = next_open_position.size -amount
        next_open_position.closed = True
        next_open_position.close_price = price
        add_close_quote_prices(next_open_position, timestamp)
        next_open_position.size = amount

        new_position = Position(next_open_position.user_id, 
                            next_open_position.baseAsset, 
                            next_open_position.quoteAsset, 
                            size_diff, 
                            next_open_position.open_timestamp, 
                            next_open_position.open_price)
        new_position.open_price_btc = next_open_position.open_price_btc           
        new_position.open_price_usd = next_open_position.open_price_usd           
        new_position.open_price_eur = next_open_position.open_price_eur           
        new_position.split_count = next_open_position.split_count+1
        db.session.add(new_position)
    
    elif next_open_position.size < amount:
        next_open_position.closed = True
        next_open_position.close_price = price
        add_close_quote_prices(next_open_position, timestamp)
        size_diff = amount -next_open_position.size
        db.session.commit()

        close_position(baseAsset, size_diff, price, timestamp)
    db.session.commit()

def add_open_quote_prices(position):
    position.open_price_btc = position.open_price * get_quote_factor(position.quoteAsset, "BTC", position.open_timestamp/1000)
    position.open_price_usd = position.open_price * get_quote_factor(position.quoteAsset, "USD", position.open_timestamp/1000)
    position.open_price_eur = position.open_price * get_quote_factor(position.quoteAsset, "EUR", position.open_timestamp/1000)

def add_close_quote_prices(position, timestamp):
    position.close_price_btc = position.close_price * get_quote_factor(position.quoteAsset, "BTC", timestamp/1000)
    position.close_price_usd = position.close_price * get_quote_factor(position.quoteAsset, "USD", timestamp/1000)
    position.close_price_eur = position.close_price * get_quote_factor(position.quoteAsset, "EUR", timestamp/1000)

def get_quote_factor(quote, target_quote, timestamp):
    if quote == target_quote:
        return 1
    
    day_seconds = 86400
    symbol = "{}/{}".format(quote, target_quote)
    price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if price:
        return price.open
    symbol = "{}/{}".format(target_quote, quote)
    reverse_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if reverse_price:
        return 1/reverse_price.open

    
    symbol = "{}/BTC".format(quote)
    quote_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if quote_price:
        quote_price_open = quote_price.open
    else:
        quote_price_open = -1

   
    symbol = "BTC/{}".format(target_quote)
    target_quote_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    
    if target_quote_price:
        target_quote_price_open = target_quote_price.open
    else:
        target_quote_price_open = -1
    
    if target_quote_price_open != -1 and quote_price_open != -1:
        return target_quote_price_open*quote_price_open
    

    return -1
    