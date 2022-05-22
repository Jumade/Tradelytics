from flask import request
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token, jwt_required
from flask_restx import Namespace, Resource, fields

from app import bcrypt
from app.api.utils import get_user_by_username, get_user_by_id, add_user, add_exchange, update_exchange, get_exchange_settings_by_id, update_user_settings, delete_exchange
from app.commands.trades import check_api_config


user_namespace = Namespace("user")

user = user_namespace.model(
    "User",
    {"username": fields.String(required=True)},
)

full_user = user_namespace.clone(
    "Full User", user, {"password": fields.String(required=True)}
)

login = user_namespace.model(
    "User",
    {"username": fields.String(required=True), "password": fields.String(required=True)},
)

refresh = user_namespace.model(
    "Refresh", {"refresh_token": fields.String(required=True)}
)

tokens = user_namespace.clone(
    "Access and refresh_tokens", refresh, {"access_token": fields.String(required=True)}
)

exchange = user_namespace.model(
    "Exchange",
    {"name": fields.String(required=True), 
    "exchange_id": fields.String(required=True),
    "apikey": fields.String(required=True),
    "apisecret": fields.String(required=True)},
)
exchange_id = user_namespace.clone(
    "Exchange_id",exchange,
    {"id": fields.Integer(required=True)},
)

parser = user_namespace.parser()
parser.add_argument("Authorization", location="headers")


class Register(Resource):
    @user_namespace.marshal_with(user)
    @user_namespace.expect(full_user, validate=True)
    @user_namespace.response(201, "Success")
    @user_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")

        user = get_user_by_username(username)
        if user:
            user_namespace.abort(400, "Sorry. That email already exists.")
        user = add_user(username, password)
        return user, 201


class Login(Resource):
    @user_namespace.marshal_with(tokens)
    @user_namespace.expect(login, validate=True)
    @user_namespace.response(200, "Success")
    @user_namespace.response(404, "User does not exist")
    def post(self):
        post_data = request.get_json()

        username = post_data.get("username")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_username(username)
        if not user or not bcrypt.check_password_hash(user.password, password):
            user_namespace.abort(404, "User does not exist")

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response_object = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response_object, 200


class Refresh(Resource):
    @user_namespace.marshal_with(tokens)
    @jwt_required(refresh=True)
    @user_namespace.response(200, "Success")
    @user_namespace.response(401, "Invalid token")
    def get(self):
        response_object = {}

        identity = get_jwt_identity()
        user = get_user_by_id(identity)

        if not user:
            user_namespace.abort(401, "Invalid token")

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response_object = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return (response_object,)

class Settings(Resource):
    @jwt_required(refresh=False)
    @user_namespace.response(200, "Success")
    @user_namespace.response(401, "Invalid token")
    def get(self):
        identity = get_jwt_identity()
        exchanges = get_exchange_settings_by_id(identity)
        
        print(exchanges)
        user = get_user_by_id(identity)
        response_object = {
            "name": user.username,
            "quote_asset_setting": user.quote_asset_setting,
            "exchanges": exchanges.to_dict('records'),
        }
        return response_object, 200

class QuoteAsset(Resource):
    @jwt_required(refresh=False)
    @user_namespace.response(200, "Success")
    @user_namespace.response(401, "Invalid token")
    def post(self):
        identity = get_jwt_identity()
        post_data = request.get_json()

        update_user_settings(identity, post_data.get("name"))
        exchanges = get_exchange_settings_by_id(identity)
        user = get_user_by_id(identity)
        response_object = {
            "name": user.username,
            "quote_asset_setting": user.quote_asset_setting,
            "exchanges": exchanges.to_dict('records'),
        }
        return response_object, 200

class Exchanges(Resource):
    @jwt_required(refresh=False)
    @user_namespace.expect(exchange, validate=True)
    @user_namespace.response(200, "Success")
    @user_namespace.response(401, "Invalid token")
    def post(self):
        identity = get_jwt_identity()
        post_data = request.get_json()

        name = post_data.get("name")
        exchange_id = post_data.get("exchange_id")
        apikey = post_data.get("apikey")
        apisecret = post_data.get("apisecret")
        valid = check_api_config(exchange_id, apikey, apisecret)
        add_exchange(identity, name, exchange_id, apikey, apisecret, valid)

        exchanges = get_exchange_settings_by_id(identity)
        user = get_user_by_id(identity)
        response_object = {
            "name": user.username,
            "quote_asset_setting": user.quote_asset_setting,
            "exchanges": exchanges.to_dict('records'),
        }
        return response_object, 200

class ExchangeUpdate(Resource):
    @jwt_required(refresh=False)
    def put(self, id):
        identity = get_jwt_identity()
        post_data = request.get_json()

        name = post_data.get("name")
        exchange_id = post_data.get("exchange_id")
        apikey = post_data.get("apikey")
        apisecret = post_data.get("apisecret")
        valid = check_api_config(exchange_id, apikey, apisecret)

        update_exchange(id, name, exchange_id, apikey, apisecret, valid)

        exchanges = get_exchange_settings_by_id(identity)
        user = get_user_by_id(identity)
        response_object = {
            "name": user.username,
            "exchanges": exchanges.to_dict('records'),
        }
        return response_object, 200
    
    @jwt_required(refresh=False)
    def delete(self, id):
        identity = get_jwt_identity()
        print("delate ex")
        delete_exchange(id)

        exchanges = get_exchange_settings_by_id(identity)
        user = get_user_by_id(identity)
        response_object = {
            "name": user.username,
            "quote_asset_setting": user.quote_asset_setting,
            "exchanges": exchanges.to_dict('records'),
        }
        return response_object, 200


user_namespace.add_resource(Register, "/register")
user_namespace.add_resource(Login, "/login")
user_namespace.add_resource(Refresh, "/refresh")
user_namespace.add_resource(Exchanges, "/exchange")
user_namespace.add_resource(Settings, "/settings")
user_namespace.add_resource(QuoteAsset, "/quote")
user_namespace.add_resource(ExchangeUpdate, "/exchange-update/<int:id>")

