import pandas as pd

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.commands.trades import build_position_data


coinlist_namespace = Namespace("coinlist")


class Portfolio(Resource):
    @jwt_required(refresh=False)
    def get(self, target_quote):
        identity = get_jwt_identity()
        trades = build_position_data(identity, target_quote)
        
        return trades, 201



coinlist_namespace.add_resource(Portfolio, "/portfolio/<string:target_quote>")
