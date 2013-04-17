"""
finder_view.py -- A flask based sun search tool

TO DO: 
	Go Live: 
		change secret key 
		turn off debug

	Currently small sample used and picking center of neighborhood. Future would be good to find a better way to apply

QUESITONS / ERROR:
	How to search and extroapolate just one word in a string of words

"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
# import model and assign to db_session variable
from sun_model import session as db_session, Coordinates
# import database model
import sun_model
# expect to need for pulling api key from environment
import os



# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
app.secret_key = 'key'

# app.config.from_object(__name__) - allows for setting all caps var as global var
# eg: SECRET_KEY = "bbbb"

@app.route('/')
def index():
	return render_template('index.html')

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
	return render_template('search.html')

# create actual search function to enter the name of the location
@app.route('/search', methods=['POST'])
def search():
	# capture the query request from the form into a variable
	question = request.form['query']
	print question
	# confirm the infromation captured matches db; otherwise throw error and ask to search again 
	# code below will account for lower and upper case
	loc_match = db_session.query(Coordinates).filter(Coordinates.n_hood.ilike("%" + question + "%")).all()
	if loc_match:
		# return the results template
		return redirect(url_for('fast_result'))
	else:
		print "Sorry, we are not covering that area at this time. Please try again."
		return redirect(url_for('search'))
	# query data model file to match name of location to lat & long and then assign to variables
	# lat_var
	# long_var
	# pull API key from env
	
	# submit lat, long and api to forecast.io and store json result into variable

	# parse json result and pull icon and tempurature data and assign to variables

	# based on icon result, return a corresponding image

	# print image and tempurature data on page

	

# create view that will show simple sun result from search
@app.route('/fast_result')
def fast_result():
	return render_template('fast_result.html')

# create an extend result view with weather details and map view

# create map view - set this up to test
@app.route('/map_view')
def map_view():
	return render_template('map_view.html')

# create login view
# create profile page view with favorites and ability report on validty of sun

# runs app
if __name__ == "__main__":
	app.run(debug=True)