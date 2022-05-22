# manage.py

import threading

import sys
import csv
from dateutil import parser

import schedule
import time
from flask.cli import FlaskGroup

from app import create_app, db
from app.api.db_models.user import User
from app.background.trades_processor import process_all_trades
from app.background.trades_loader import load_trades
from app.background.price_loader import load_daily_prices

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()

    # load user table
    db.session.add(User(username='admin', password="admin"))

    db.session.commit()
    print("database reset done!")

@cli.command('process_trades')
def process_trades_command():
    process_all_trades()

@cli.command('load_exchange_trades')
def load_exchange_trades():
    load_trades()

@cli.command('load_daily_prices')
def load_daily():
    load_daily_prices()

@cli.command('run_schedule')
def run_schedule():
    schedule.every(5).minutes.do(background_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def background_job():
    print("--- run job ---")
    with app.app_context():
        try:
            load_trades()
            load_daily_prices()
            process_all_trades()
        except Exception as e:
            print(e) 


if __name__ == '__main__':
    cli()
