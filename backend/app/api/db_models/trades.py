import datetime
import os

from flask import current_app
from sqlalchemy.sql import func

from app import bcrypt, db


class Trade(db.Model):
    __tablename__ = "trades"

    id = db.Column(db.String(255), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    exchange = db.Column(db.String(255), nullable=False)

    timestamp = db.Column(db.BigInteger, nullable=False)
    symbol = db.Column(db.String(255), nullable=False)
    baseAsset = db.Column(db.String(255), nullable=False)
    quoteAsset = db.Column(db.String(255), nullable=False)

    side = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    processed = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, data, user_id, exchange):
        self.user_id = user_id
        self.exchange = exchange
        self.id = data["id"]
        self.timestamp = data["timestamp"]
        self.symbol = data["symbol"]

        assets = data["symbol"].split("/")
        self.baseAsset = assets[0]
        self.quoteAsset = assets[1]

        self.side = data["side"]
        self.price = data["price"]
        self.amount = data["amount"]
        self.cost = data["cost"]
        
