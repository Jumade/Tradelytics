from flask_restx import Api

from app.api.user import user_namespace
from app.api.coinlist import coinlist_namespace

api = Api(version="1.0", title="CB APIs", doc="/docs/")

api.add_namespace(user_namespace, path="/user")
api.add_namespace(coinlist_namespace, path="/coinlist")
