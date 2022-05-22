import datetime
import os

from flask import current_app
from sqlalchemy.sql import func

from app import bcrypt, db


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    quote_asset_setting = db.Column(db.String(255), default="BTC", nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username="", password="", quote_asset_setting="BTC"):
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
        self.quote_asset_setting = quote_asset_setting
