from app import db
from app.api.db_models.user import User
from app.api.db_models.exchange import Exchange
import pandas as pd
import numpy as np


def get_user_by_id(user_id):
    t = User.query.filter_by(id=user_id).first()
    return t

def get_exchange_settings_by_id(id):
    query = Exchange.query.filter_by(user_id=id)
    exchanges =  pd.read_sql(query.statement, query.session.bind)
    exchanges['last_trades_update'] = pd.to_datetime(exchanges['last_trades_update'], errors='coerce')
    exchanges['last_price_update'] = pd.to_datetime(exchanges['last_price_update'], errors='coerce')
    exchanges["last_trades_update"] = exchanges["last_trades_update"].dt.strftime('%Y-%m-%d %X')
    exchanges["last_price_update"] = exchanges["last_price_update"].dt.strftime('%Y-%m-%d %X')
    exchanges.replace(np.nan,"", inplace=True)
    return exchanges


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
    

def add_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def add_exchange(user_id, name, exchange_id, apikey, apisecret, valid):
    exchange = Exchange(user_id, name, exchange_id, apikey, apisecret, valid)
    db.session.add(exchange)
    db.session.commit()
    return exchange

def update_user_settings(id, quote_asset_setting):
    User.query.filter_by(id=id).update({User.quote_asset_setting: quote_asset_setting})
    db.session.commit()

def update_exchange(id, name, exchange_id, apikey, apisecret, valid):
    Exchange.query.filter_by(id=id).update({Exchange.name: name, 
                                            Exchange.exchange_id: exchange_id, 
                                            Exchange.apikey: apikey, 
                                            Exchange.apisecret: apisecret,
                                            Exchange.valid: valid})
    db.session.commit()


def delete_exchange(id):
    Exchange.query.filter_by(id=id).delete()
    db.session.commit()

