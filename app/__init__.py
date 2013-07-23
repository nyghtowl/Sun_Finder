import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask.ext.login import LoginManager
from config import engine


# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
#app.secret_key = os.environ.get('flask_key')
app.secret_key = os.environ.get('key')
app.config.from_object(__name__) # allows for setting all caps var as global var

# variable represents sqlalchemy
db = SQLAlchemy(app)

# opens on ongoing session with db
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# class that connects to the declarative_base of sqlalchemy
Base = declarative_base()
Base.query = session.query_property()


#login information
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect non-loggedin users to login screen
login_manager.login_view = "login" # result if user not logged in
login_manager.login_message = u"Login to customize your weather view."

from app import views, models