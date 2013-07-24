import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


# Initialize Flask app
app = Flask(__name__)

app.config.from_object('config') 

# Variable represents sqlalchemy
db = SQLAlchemy(app)

# Login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

from app import views, models