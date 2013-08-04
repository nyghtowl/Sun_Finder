# Config
# -*- coding: utf-8 -*-

import os

from signal import signal, SIGPIPE, SIG_DFL 
#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE,SIG_DFL) 


# Move functions out of model that run model into config

# Pull weather api keys
G_KEY = os.environ.get('G_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

SECRET_KEY = os.environ.get('key')

CSRF_ENABLED = True

basedir = os.path.abspath(os.path.dirname(__file__))

# Code to setup a postgres database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/sun_finder_db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


# Stores migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


