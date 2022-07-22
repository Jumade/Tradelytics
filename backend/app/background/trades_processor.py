
from app import db
from app.api.db_models.trades import Trade
from app.api.db_models.positions import Position
from app.api.db_models.daily_price import DailyPrice
from app.api.db_models.user import User

def process_all_trades():
    users = User.query.all()
    for user in users:
        process_trades(user.id)

def clean_positions(user_id):
    query = Trade.query.filter_by(processed=False, user_id=user_id).order_by(Trade.timestamp.asc())
    trades = query.all()
    for trade in trades:
        trades_by_baseAsset = Trade.query.filter_by(baseAsset=trade.baseAsset, user_id=user_id).order_by(Trade.timestamp.asc()).all()
        for trade_by_baseAsset in trades_by_baseAsset:
            trade_by_baseAsset.processed = False
        db.session.query(Position).filter_by(baseAsset=trade.baseAsset, user_id=user_id).delete()
    db.session.commit()

def process_trades(user_id):
    clean_positions(user_id)
    
    query = Trade.query.filter_by(processed=False, user_id=user_id).order_by(Trade.timestamp.asc())
    trades = query.all()
    for trade in trades:
        if trade.side == "buy":
            open_position(trade)
        elif trade.side == "sell":
            close_position(trade.baseAsset, trade.amount, trade.price,  trade.quoteAsset, trade.timestamp)
        trade.processed = True
    db.session.commit()

def open_position(trade):
    position = Position(trade.user_id, trade.baseAsset, trade.amount, trade.timestamp)
    add_open_quote_prices(position, trade.price,  trade.quoteAsset, trade.timestamp)
    db.session.add(position)
    db.session.commit()


def close_position(baseAsset, amount, price, quoteAsset, timestamp):
    next_open_position = Position.query.filter_by(baseAsset=baseAsset, closed=False).order_by(Position.open_timestamp.asc(), Position.split_count.asc()).first()
    if next_open_position == None:
        return
    if next_open_position.size == amount:
        next_open_position.closed = True
        add_close_quote_prices(next_open_position, price, quoteAsset, timestamp)
    elif next_open_position.size > amount:
        size_diff = next_open_position.size -amount
        next_open_position.closed = True
        add_close_quote_prices(next_open_position, price, quoteAsset, timestamp)
        next_open_position.size = amount

        new_position = Position(next_open_position.user_id, 
                            next_open_position.baseAsset, 
                            size_diff, 
                            next_open_position.open_timestamp)
        new_position.open_price_btc = next_open_position.open_price_btc           
        new_position.open_price_usd = next_open_position.open_price_usd           
        new_position.open_price_eur = next_open_position.open_price_eur           
        new_position.split_count = next_open_position.split_count+1
        db.session.add(new_position)
    
    elif next_open_position.size < amount:
        next_open_position.closed = True
        add_close_quote_prices(next_open_position, price, quoteAsset, timestamp)
        size_diff = amount -next_open_position.size
        db.session.commit()

        close_position(baseAsset, size_diff, price, quoteAsset, timestamp)
    db.session.commit()

def add_open_quote_prices(position, open_price, quoteAsset, open_timestamp):
    position.open_price_btc = open_price * get_quote_factor(quoteAsset, "BTC", open_timestamp/1000)
    position.open_price_usd = open_price * get_quote_factor(quoteAsset, "USD", open_timestamp/1000)
    position.open_price_eur = open_price * get_quote_factor(quoteAsset, "EUR", open_timestamp/1000)

def add_close_quote_prices(position, close_price, quoteAsset, timestamp):
    position.close_price_btc = close_price * get_quote_factor(quoteAsset, "BTC", timestamp/1000)
    position.close_price_usd = close_price * get_quote_factor(quoteAsset, "USD", timestamp/1000)
    position.close_price_eur = close_price * get_quote_factor(quoteAsset, "EUR", timestamp/1000)

def get_quote_factor(quote, target_quote, timestamp):
    if quote == target_quote:
        return 1
    
    day_seconds = 86400
    symbol = "{}/{}".format(quote, target_quote)
    price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if price:
        return price.open
    symbol = "{}/{}".format(target_quote, quote)
    reverse_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if reverse_price:
        return 1/reverse_price.open

    
    symbol = "{}/BTC".format(quote)
    quote_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    if quote_price:
        quote_price_open = quote_price.open
    else:
        quote_price_open = -1

   
    symbol = "BTC/{}".format(target_quote)
    target_quote_price = DailyPrice.query.filter(DailyPrice.timestamp  <= timestamp,
                                        DailyPrice.timestamp + day_seconds  > timestamp,
                                        DailyPrice.symbol == symbol).first()
    
    if target_quote_price:
        target_quote_price_open = target_quote_price.open
    else:
        target_quote_price_open = -1
    
    if target_quote_price_open != -1 and quote_price_open != -1:
        return target_quote_price_open*quote_price_open
    

    return -1
    