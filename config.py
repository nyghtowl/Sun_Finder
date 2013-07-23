import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# pull api keys from environment
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

# code to setup a postgres database
database_url = os.getenv('HEROKU_POSTGRESQL_GOLD_URL', 'postgresql://localhost/sun_model')
ENGINE = create_engine(database_url, echo=True) # Shows translations till put to False

# opens on ongoing session with db
DB_SESSION = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

