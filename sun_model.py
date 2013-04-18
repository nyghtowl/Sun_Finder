"""
sun_model.db holds code to setup and reference related databases 

applying sqlalchemy

Go Live: set echo back to False

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, types
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, scoped_session

# variable represents connecting to db
engine = create_engine("sqlite:///sun_finder.db", echo=True)

# opens on ongoing session with db
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# class that connects to teh declarative_base of sqlalchemy
Base = declarative_base()
Base.query = session.query_property()

# create class and table for locations
class Location(Base):
	__tablename__="location"

	id = Column(Integer, primary_key=True)
	lati = Column(Float) # don't set a limit on size of float - apply to when output
	longi = Column(Float)
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