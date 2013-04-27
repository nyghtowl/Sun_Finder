"""
finder_view.py -- A flask based sun search tool

TO DO: 
	Go Live: 
		change secret key 
		turn off debug

	Currently small sample used and picking center of neighborhood. Future would be good to find a better way to apply

	Need to add neighborhood to query - still not perfect but will help center
	Set radius and cetnral coordinates to cover bay area
	Can set a loop to compare coordinates for closest to the central ones for neighborhood in local db?

QUESITONS / ERROR:
	Need to review with someone url_for application for css and js http://flask.pocoo.org/docs/patterns/jquery/

TOP TO DO:
	Create WT form and Login...
	Finish linking up just date
	Put text and links on map
	Setup map to pop-up on first page and allow selection of neighborhood for autocomplete
	
	Build out autocomplete w/ Liz direction
	ajax - send off request and use ajax to pull in bits to load

	setup ability to choose time

	polygon file - aquire for neihborhood - google maps has a way to apply polygon shape and make clickable
	flask login



"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
# import model and assign to db_session variable
from sun_model import session as db_session, Location
# import database model
import sun_model
# expect to need for pulling api key from environment
import os
# leverage for reporting time result
import datetime
import time
import sun_functions
import weather_forecast

# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
#app.secret_key = os.environ.get('flask_key')
app.secret_key = 'key'

app.config.from_object(__name__) # allows for setting all caps var as global var

# pull api keys from environment
G_KEY = os.environ.get('G_KEY')
FIO_KEY = os.environ.get('FIO_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

@app.route('/')
def index():
	return redirect(url_for('search'))

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
	return render_template('search.html')

# create search function 
@app.route('/search', methods=['POST'])
def search():
	#session.pop('forecast', None)

	# capture the form results
	txt_query = request.form['query']
	
	# FIX - search by specif time

	date_query = request.form['date']

	# determine date captured to utilize
	if not(date_query):
		as_of = datetime.datetime.now()
	else:
		#grabs date that is entered and combines with automatically generated time
		#FIX - all entering time
		as_of_time = datetime.datetime.now().time()
		as_of_date = datetime.datetime.strptime(date_query, "%Y-%m-%d")
		as_of = datetime.datetime.combine(as_of_date,as_of_time)
	
	# pull coordinates from Google Places
	forecast_result = sun_functions.get_coord(txt_query, G_KEY, FIO_KEY, WUI_KEY)
	
	#FIX - push certain results back to Google Places to improve weigh results for neighborhoods & potentially still use local db on neighborhoods

	# validate there are coordinates and then get the forecast
	if forecast_result:
		forecast_result.validate_day(as_of)
		#x_test = validate_day_test(get_forecast_test(coord_result['lat'],coord_result['lng']))

		#forecast_result['loc_name'] = txt_query.title()
		session['forecast'] = forecast_result
		#print session["forecast"]

		return render_template('fast_result.html', result = forecast_result)
	
	#FIX flash a message to try search again if coord_result is not valid

	'''
	First Solution: Utilizing sample local db - may still use

	# query data model file to match name of location to lat & long and then assign to variables
	loc_match = db_session.query(Location).filter(Location.n_hood.ilike("%" + question + "%")).one()
	
	# confirm the infromation captured matches db; otherwise throw error and ask to search again 
	if loc_match:
		# if there is a match the pass to get forecast, validate its day and then get elements to pop results
		forecast_result = validate_day(get_forecast(loc_match))
		forecast_result['loc_name'] = question.title()
		#return redirect(url_for('fast_result'), result=forecast_result)
		return render_template('fast_result.html', result = forecast_result)
	else:
		# FIX using flash or a result on the html page...
		print "Sorry, we are not covering that area at this time. Please try again."
		return redirect(url_for('search'))
	'''

	# FIX add image and tempurature to a dictionary that is passed to page

# FIX - session not working

# create extended view that of weather results (Note need trailing slash to avoid 404 error if web page access trys to add it)
@app.route('/more_details/')
def more_details():
	forecast_details = session.get('forecast')
	print forecast_details
	#print forecast_details
 	return render_template('more_details.html', details=forecast_details)

# create an extend result view with weather details and map view

# create map view - set this up to test
@app.route('/map_view')
def map_view():
	return render_template('map_view.html')

# Below were used to test session variable and prove its working
@app.route("/test1")
def test1():
	session['forecast'] = 5

	session['squid'] = 5
	return ""

@app.route("/test2")
def test2():
	print session
	return ""

# create login view
# create profile page view with favorites and ability report on validty of sun

# runs app
if __name__ == "__main__":
	app.run(debug=True)