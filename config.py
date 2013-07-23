import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Move functions out of model that run model into config

# pull api keys from environment
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))

# code to setup a postgres database
SQLALCHEMY_DB_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://' + os.path.join(basedir, 'sun_model.db'))
ENGINE = create_engine(SQLALCHEMY_DB_URI, echo=True) # Shows translations till put to False

# opens on ongoing session with db
DB_SESSION = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

