#!/usr/bin/env python3
"""Simple Flask app config"""

import pathlib

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, static_url_path='/static', static_folder='static')

import secrets


def create_app():
    """Create Flask app"""
    this_app = Flask(__name__)
    this_app.config['SECRET_KEY'] = 'your_secret_key_here'
    if not pathlib.Path(".flaskenv").exists():
        load_dotenv(pathlib.Path(__file__).parent / pathlib.Path(".flaskenv"))
    this_app.config.from_prefixed_env()
    return this_app


app = create_app()

app.config['static_folder'] = 'static'

this_dir = pathlib.Path(__file__).parent
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + str(
    this_dir / pathlib.Path("farm.sqlite3")
)

db = SQLAlchemy(app)

ma = Marshmallow(app)
