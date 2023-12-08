import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

# SQl database path
sql_database_path = os.path.join(os.path.dirname(__file__),
                                 "data/db/database.db")

# App config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" +\
    sql_database_path
app.config["SOLALCHEMY TRACK MODIFICATIONS"] = False
app.config["SQLALCHEMY ECHO"] = True

# database object
db = SQLAlchemy(app)