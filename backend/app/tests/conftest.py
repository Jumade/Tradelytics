
import pytest

from app import create_app, db
from app.api.db_models.user import User
from app.api.db_models.trades import Trade
from app.api.db_models.exchange import Exchange
from app.api.db_models.daily_price import DailyPrice


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def add_user():
    def _add_user(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user

@pytest.fixture(scope="module")
def add_trade():
    def _add_trade(user_id, exchange, baseAsset, quoteAsset, id, timestamp, side, price, amount):
        data = {}
        data["id"] = id
        data["timestamp"] = timestamp
        data["symbol"] = "{}/{}".format(baseAsset, quoteAsset)
        data["side"] = side
        data["price"] = price
        data["amount"] = amount
        data["cost"] = amount * price
        trade = Trade(data, user_id, exchange)
        db.session.add(trade)
        db.session.commit()
        return trade

    return _add_trade

@pytest.fixture(scope="module")
def add_exchange():
    def _add_exchange(user_id, name, exchange_id, apikey, apisecret, valid):
        exchange = Exchange(user_id, name, exchange_id, apikey, apisecret, valid)
        db.session.add(exchange)
        db.session.commit()
        return exchange

    return _add_exchange

@pytest.fixture(scope="module")
def add_daily_price():
    def _add_daily_price(symbol, timestamp, open, high, low, close, exchange_id):
        price = DailyPrice( symbol, timestamp, open, high, low, close, exchange_id)
        db.session.add(price)
        db.session.commit()
        return price

    return _add_daily_price

