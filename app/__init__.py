import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import DB_SESSION


# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)

app.config.from_object('config') 

# variable represents sqlalchemy
db = SQLAlchemy(app)

#login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

from app import views, models