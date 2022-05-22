
import time
import os
import sys
from app import db
from app.api.db_models.trades import Trade
from sqlalchemy import or_
from sqlalchemy.sql import func

import datetime 


import ccxt  
from app.api.db_models.exchange import Exchange

def load_trades():
    current_time = datetime.datetime.utcnow()
   
    day_ago = current_time - datetime.timedelta(days=1)
    query = Exchange.query.filter_by(valid=True, active=True).filter(or_(Exchange.last_trades_update < day_ago, Exchange.last_trades_update== None))
    echanges = query.all()
    for echange in echanges:
        print("update trades", echange.exchange_id)
        try:
            exchange_class = getattr(ccxt, echange.exchange_id)
            exchange = exchange_class({
                'apiKey': echange.apikey,
                'secret': echange.apisecret,
                'enableRateLimit': True,
            })
        
            exchange.load_markets ()
            markets = exchange.fetch_markets ()
            for symbol_data in markets:
                baseAsset = symbol_data["base"]
                quoteAsset = symbol_data["quote"]
                symbol = "{}/{}".format(baseAsset, quoteAsset)
                print(symbol)
                

                # exchange.verbose = True  # uncomment for debugging
                
                from_id = '0'
                params = { 'fromId': from_id }
                previous_from_id = from_id

                all_trades = []

                while True:

                    print('------------------------------------------------------------------')
                    print('Fetching with params', params)
                    trades = exchange.fetch_my_trades(symbol, None, None, params)
                    print('Fetched', len(trades), 'trades')
                    if len(trades):
                        last_trade = trades[len(trades) - 1]
                        if last_trade['id'] == previous_from_id:
                            break
                        else:
                            previous_from_id = last_trade['id']
                            params['fromId'] = last_trade['id']
                            all_trades = all_trades + trades
                    else:
                        break
                print('Fetched', len(all_trades), 'trades')
                for i in range(0, len(all_trades)):
                    trade = all_trades[i]
                    print (i, trade['id'], trade['datetime'], trade['amount'])
                    print (i, trade)
                    trade = Trade(trade, echange.user_id, echange.exchange_id)
                    db.session.merge(trade)
                
                db.session.commit()
            
            Exchange.query.filter_by(id=echange.id).update({Exchange.last_trades_update:func.now()})
            db.session.commit()
        except Exception as e:
            print(e)    
