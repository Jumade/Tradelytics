import datetime
import os

from flask import current_app
from sqlalchemy.sql import func

from app import bcrypt, db


class Position(db.Model):
    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    split_count = db.Column(db.Integer,default=0, nullable=False)

    baseAsset = db.Column(db.String(255), nullable=False)
    quoteAsset = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Float, nullable=False)

    open_timestamp = db.Column(db.BigInteger, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    open_price_btc = db.Column(db.Float, nullable=True)
    open_price_usd = db.Column(db.Float, nullable=True)
    open_price_eur = db.Column(db.Float, nullable=True)

    close_price = db.Column(db.Float, nullable=True)
    close_price_btc = db.Column(db.Float, nullable=True)
    close_price_usd = db.Column(db.Float, nullable=True)
    close_price_eur = db.Column(db.Float, nullable=True)

    closed = db.Column(db.Boolean, default=False, nullable=False)
    

    def __init__(self, user_id, baseAsset, quoteAsset, size, open_timestamp, open_price):
        self.user_id = user_id
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.size = size
        self.open_timestamp = open_timestamp
        self.open_price = open_price
        
        
