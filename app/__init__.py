import os
from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import LoginManager
from config import DB_SESSION


# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
#app.secret_key = os.environ.get('flask_key')
app.secret_key = os.environ.get('key')

app.config.from_object('config') 

# variable represents sqlalchemy
# db = SQLAlchemy(app)

# class that connects to the declarative_base of sqlalchemy
Base = declarative_base()
Base.query = DB_SESSION.query_property()

#login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

from app import views, models