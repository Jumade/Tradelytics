from dataclasses import dataclass
import datetime
import os

from flask import current_app
from sqlalchemy.sql import func

from app import bcrypt, db

@dataclass
class Exchange(db.Model):

    __tablename__ = "exchange"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(128), nullable=False)
    exchange_id = db.Column(db.String(128), nullable=False)
    apikey = db.Column(db.String(128), nullable=False)
    apisecret = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    valid = db.Column(db.Boolean(), default=False, nullable=False)
    last_trades_update = db.Column(db.DateTime, nullable=True)
    last_price_update = db.Column(db.DateTime, nullable=True)


    def __init__(self, user_id, name, exchange_id, apikey, apisecret, valid):
        self.user_id = user_id
        self.exchange_id = exchange_id
        self.name = name
        self.apikey = apikey
        self.apisecret = apisecret
        self.valid = valid
