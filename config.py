# -*- coding: utf-8 -*-

import os

# Move functions out of model that run model into config

# Pull weather api keys
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

SECRET_KEY = os.environ.get('key')

CSRF_ENABLED = True

basedir = os.path.abspath(os.path.dirname(__file__))

# Code to setup a postgres database
# SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.path.join(basedir, 'sun_model_db')
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/sun_finder_db'
# SUN_MODEL = 'postgresql://' + os.path.join(basedir, 'sun_model_db')

# Code to pull postgres db or local db
# SQLALCHEMY_DB_URI = os.environ['DATABASE_URL']
# SQLALCHEMY_DATABASE_URI = os.getenv(os.environ['DATABASE_URL'], SUN_MODEL)

# Stores migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_respository')


