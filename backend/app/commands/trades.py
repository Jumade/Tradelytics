
import time
import os
import sys
from app import db
import pandas as pd
from app.api.db_models.trades import Trade
from app.api.db_models.positions import Position
from app.api.db_models.daily_price import DailyPrice
from sqlalchemy import or_
from sqlalchemy.sql import func

import datetime 

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
import cryptocompare

import ccxt  
from app.api.db_models.exchange import Exchange


def get_positions_by_user(id):
    query = Position.query.filter_by(user_id=id)
    return pd.read_sql(query.statement, query.session.bind)

def build_position_data(user_id, target_quote):
    positions_df = get_positions_by_user(user_id)
    positions_df["open_cost"] = positions_df["open_price_{}".format(target_quote.lower())] * positions_df["size"]
    positions_df["close_cost"] = positions_df["close_price_{}".format(target_quote.lower())] * positions_df["size"]
    positions_df["unrealized_open_cost"] = positions_df[((positions_df["closed"] == False))]["open_cost"]

    load_current_price(positions_df, target_quote)
    positions_df["unrealized_close_cost"] = positions_df[((positions_df["closed"] == False))]["current_price"] * positions_df["size"]
 
    positions_df["realized_pl"] = positions_df["close_cost"] - positions_df["open_cost"]
    positions_df["unrealized_pl"] = positions_df["unrealized_close_cost"] - positions_df["unrealized_open_cost"]



    f = dict.fromkeys(positions_df, 'sum')
    f.update(dict.fromkeys(positions_df.columns[positions_df.dtypes.eq(object)], 'first'))
    positions_df = positions_df.groupby(["baseAsset"], as_index=False).agg(f)

    
    positions_df["realized_pl_perc"] = positions_df["realized_pl"] / positions_df["open_cost"]
    positions_df["unrealized_pl_perc"] = positions_df["unrealized_pl"] / positions_df["unrealized_open_cost"]
    positions_df["total_pl"] = positions_df["unrealized_pl"] + positions_df["realized_pl"]
    positions_df["total_pl_perc"] = positions_df["total_pl"] / (positions_df["open_cost"] + positions_df["unrealized_open_cost"])

    positions_df.sort_values(by=['unrealized_open_cost'], inplace=True, ascending=False)
    return positions_df.to_dict('records')

def load_current_price(positions_df, target_quote):
    unique_assets = positions_df["baseAsset"].unique()
    positions_df["current_price"] = 0.0
    prices = cryptocompare.get_price(list(unique_assets), [target_quote])
    for key, value in prices.items():
        positions_df.loc[positions_df["baseAsset"] == key, "current_price"] = value[target_quote]

def check_api_config(exchange_id, apiKey, secret):
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': apiKey,
            'secret': secret,
        })
        balance = exchange.fetch_balance()
    except Exception as e:
        print(e)
        return False

    
    return True