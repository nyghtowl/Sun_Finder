#!flask/bin/python

from app import app
import os

port = int(os.environ.get('PORT', 5000))
app.run(debug = False, host = '0.0.0.0', port=port)
