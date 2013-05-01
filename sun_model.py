"""
sun_model.db holds code to setup and reference related databases 

applying sqlalchemy

Go Live: set echo back to False

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref


# variable represents connecting to db
#engine = create_engine("sqlite:///sun_finder.db", echo=True)
# code to setup a postgres database
engine = create_engine('postgresql://localhost/sun_finder_db', echo=True)

# opens on ongoing session with db
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# class that connects to teh declarative_base of sqlalchemy
Base = declarative_base()
Base.query = session.query_property()

# create class and table for users
class User(Base):
    __tablename__ = "users"

    # creates user columns, nullable = False means its required
    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    fname = Column(String(64), nullable=False)
    lname = Column(String(64), nullable=True)
    mobile = Column(String(15), nullable=True)
    zipcode = Column(Integer, nullable=True)
    # accept terms of service
    accept_tos = Column(Boolean, unique=False, default=False)
    # track when the user created the account
    timestamp = Column(String(64), nullable=False)
   
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
class Location(Base):
    __tablename__="location"

    id = Column(Integer, primary_key=True)
    lat = Column(Float) # don't set a limit on size of float - apply to when output
    lng = Column(Float)
    rad = Column(Integer)
    n_hood = Column(String(128))

# setting this up to generate the db when main is run directly from the command line
def main():
    Base.metadata.create_all(engine)
    

# passes back session for seeding the db
def connect():
    # passes back session for seeding the db
    return session()

if __name__ == "__main__":
    main()