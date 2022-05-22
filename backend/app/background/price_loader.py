
import time
import os
import sys
from app import db
import pandas as pd
from app.api.db_models.trades import Trade
from app.api.db_models.daily_price import DailyPrice
from sqlalchemy import func
import datetime 
from sqlalchemy import or_
from sqlalchemy.sql import func
import cryptocompare


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  
from app.api.db_models.exchange import Exchange

def load_daily_prices():
    quote_targets = ["BTC", "USD", "EUR"]
    first_trade = db.session.query(func.min(Trade.timestamp)).first()
    print(first_trade[0])
    targets_pairs = quote_targets_pairs(quote_targets)
    print(targets_pairs)

    current_time = datetime.datetime.utcnow()

    day_ago = current_time - datetime.timedelta(days=1)
    scrape_candles_to_database(first_trade[0], targets_pairs)

def quote_targets_pairs(quote_targets):
    symboles = []

    trade_quotes = db.session.query(Trade.quoteAsset).group_by(Trade.quoteAsset).all()
    trade_quotes = [i[0] for i in trade_quotes]
    quote_targets = set(quote_targets) | set(trade_quotes)
    print("trade_quotes", quote_targets)

    for target in quote_targets:
        for target2 in quote_targets:
            if target != target2:
                symbol = "{}/{}".format(target, target2)
                symboles.append(symbol)

    for target in quote_targets:
        if target != "BTC":
            symbol = "BTC/{}".format(target)
            if symbol not in symboles:
                symboles.append(symbol)
    
    base_assets = db.session.query(Trade.baseAsset).distinct().all()
    for base in base_assets:
        base = base[0]
        if base != "BTC":
            symbol = "{}/{}".format(base, "BTC")
            if base != target and symbol not in symboles:
                symboles.append(symbol)

    
   
    return symboles


def scrape_candles_to_database(since, targets_pairs):
    since -= (24*60*60*1000)+1
    for targets_pair in targets_pairs:
        targets_pair_split = targets_pair.split("/")

        last_price = db.session.query(func.max(DailyPrice.timestamp)).filter_by(symbol=targets_pair).first()
        since_max = since
        if last_price[0]:
            since_max = max(since, (last_price[0]*1000)+1)
            

        from_date = since_max/1000
        ohlcv = get_historical_price_day_from(targets_pair_split[0], targets_pair_split[1], fromTs=from_date)
        
        for row in ohlcv:
            price = DailyPrice(targets_pair, row["time"], row["open"], row["high"], row["low"], row["close"], "exchange_id")
            db.session.add(price)
        db.session.commit()
        if  len(ohlcv) >0:
            print('Saved', targets_pair, len(ohlcv), 'candles from', ohlcv[0]["time"], 'to', ohlcv[-1]["time"])
        else:
            print("market does not exist", targets_pair)

def get_historical_price_day_from(coin: str, currency: str,
                                 fromTs: int = 0, delay: float = 0.2):
   
    allHist: List[Dict] = []
    toTs_i = time.time()
    fromTs_i = fromTs

    while fromTs_i <= toTs_i:
        p = cryptocompare.get_historical_price_day(coin,currency, toTs=toTs_i)
        if p is None:
            return None

        validHist = [elem for elem in p if elem['time'] >= fromTs_i and elem['open'] != 0 and elem['close'] != 0]
        allHist = validHist + allHist
        if len(validHist) < len(p):
            break
        toTs_i = (min(p, key = lambda x:x['time']))['time'] - 1
        time.sleep(delay)

    return allHist


