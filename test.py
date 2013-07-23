#!flask/bin/python
# -*- coding: utf8 -*-

import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Location

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname = 'john', email = 'john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

