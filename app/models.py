"""
sun_model.db holds code to setup and reference related databases 

applying sqlalchemy

Go Live: set echo back to False

"""
from app import db
import os

ROLE_USER = 0
ROLE_ADMIN = 1

# create class and table for users
class User(db.Model):
    __tablename__ = "users"

    # creates user db.columns, nullable = False means its required
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    # accept terms of service
    accept_tos = db.Column(db.Boolean, unique=False, default=True)
    # track when the user created the account
    timestamp = db.Column(db.String(64), nullable=False)
   
    #methods below for the Flask-login to work

    #returns true if user provides valid credentials
    def is_authenticated(self):
        return True

    # #returns true if the account is active and not suspended
    def is_active(self):
        return True

    # #returns true if anonymouse user
    def is_anonymous(self):
        return False

    # #uniquely identifies the user and can be used to load the user from the user_loader callback. Must be unicode and must conver id if int
    def get_id(self):
        return unicode(self.id)

    # used to print human readable presentation of an object - for testing purposes
    def __repr__(self):
        return '<User %r' % (self.name)

# create class and table for locations
class Location(db.Model):
    __tablename__="location"

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float) # don't set a limit on size of db.float - apply to when output
    lng = db.Column(db.Float)
    rad = db.Column(db.Integer)
    n_hood = db.Column(db.String(128))

    # FIX - figure out how to create a function out of comparing query txt to list of neighborhoods and return lat & lng
    #def query_match(self, txt):

        # if self.n_hood == txt:
        #     return (self.lat, self.lng)
    
    # used to print human readable presentation of an object - for testing purposes
    def __repr__(self):
        return '<Location %r' % (self.n_hood)

# # passes back session for seeding the db
# def connect():
#     # passes back session for seeding the db
#     return DB_SESSION()
