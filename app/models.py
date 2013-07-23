"""
Models.db 

"""
from app import db
# Secure hash
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    __tablename__ = "users"

    # Creates user db.columns, nullable = False means its required
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    # Accept terms of service
    accept_tos = db.Column(db.Boolean, unique=False, default=True)
    # Track when the user created the account
    timestamp = db.Column(db.String(64), nullable=False)
   
    # Flask-login methods

    # Return true unless user not allowed to authenticate
    def is_authenticated(self):
        return True

    # Returns False for a banned user
    def is_active(self):
        return True

    # Return true for fake users not supposed to login
    def is_anonymous(self):
        return False

    # Generate unique id for user 
    def get_id(self):
        return unicode(self.id)

    # Gravatar field
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    # Testing purposes
    def __repr__(self):
        return '<User %r' % (self.name)

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
    
    # Testing purposes
    def __repr__(self):
        return '<Location %r' % (self.n_hood)

# # passes back session for seeding the db
# def connect():
#     # passes back session for seeding the db
#     return DB_SESSION()
