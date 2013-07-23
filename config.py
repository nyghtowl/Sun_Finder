import os
from sqlalchemy import create_engine

# pull api keys from environment
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

# code to setup a postgres database
database_url = os.getenv('HEROKU_POSTGRESQL_GOLD_URL', 'postgresql://localhost/app/sun_finder_db')
engine = create_engine(database_url, echo=True) # Shows translations till put to False

