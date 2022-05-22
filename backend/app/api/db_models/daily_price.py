import datetime
import os

from flask import current_app
from sqlalchemy.sql import func

from app import bcrypt, db

class DailyPrice(db.Model):

    __tablename__ = "daily_prices"

    timestamp = db.Column(db.Integer, primary_key=True, nullable=False)
    symbol = db.Column(db.String(32), primary_key=True, nullable=False)
    exchange_id = db.Column(db.String(128), primary_key=True, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    

    def __init__(self, symbol, timestamp, open, high, low, close, exchange_id):
        self.symbol = symbol
        self.timestamp = timestamp
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.exchange_id = exchange_id
