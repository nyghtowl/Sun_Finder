import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from redis import Redis
from momentjs import momentjs 

# Initialize Flask app
app = Flask(__name__)

app.config.from_object('config')

# Variable represents sqlalchemy
db = SQLAlchemy(app)

# Initial redis instance and link to app
redis_db = Redis()

# Login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

# Hook up momentjs to jinja
app.jinja_env.globals['momentjs'] = momentjs

from app import views, models