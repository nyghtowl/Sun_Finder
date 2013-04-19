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
from sun_model import session as db_session, Location
# import database model
import sun_model
# use requests to pull information from api requests - alternative is urllib - this is more human
import requests
# expect to need for pulling api key from environment
import os
# leverage for reporting time result
import datetime
import time

# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
app.secret_key = 'key'

app.config.from_object(__name__) # allows for setting all caps var as global var
# eg: SECRET_KEY = "bbbb"

# pull api key for forecast.io
FIO_KEY = os.environ.get('FIO_KEY')

@app.route('/')
def index():
	return redirect(url_for('search'))

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
	return render_template('search.html')

# submit lat, long and api key and store json/dicationary result into variable
def get_forecast(location):
    lat = location.lati
    lon = location.longi
    url="https://api.forecast.io/forecast/%s/%f,%f"
	# pull API key from env with FIO_KEY
    final_url=url%(FIO_KEY, lat,lon)
    print final_url
    response = requests.get(final_url)
    return response.json()

# convert icon result to an image
def w_pic(icon):
	pic_location = "/static/img/"
	# holds weather images for reference
	weather_pics = {
		"clear-day":"sun_samp2.jpeg", 
		"rain":"rain.png" , 
		"snow":"snow.png", 
		"sleet":"sleet2.png", 
		"fog":"foggy2.png" , 
		"cloudy":"cloudy.png", 
		"partly-cloudy-day":"partly_cloudy.png"
	}
	
	# FIX how to handle wind icon result - determine percent cloud cover? and 
	
	if icon in weather_pics:
		#print weather_pics[icon]
		final_pic_loc = pic_location + weather_pics[icon]
		print final_pic_loc
	
	#FIX - what happends if not result

	return final_pic_loc

# pulls forecast information from work on incorporating as_of
def validate_day(forecast_info):
	
	print forecast_info['hourly']['icon']
	
	# get actual time and compare on whether it is day
	ts = int(time.time())
	sunrise_ts = int(forecast_info['daily']['data'][0]['sunriseTime'])
	sunset_ts = int(forecast_info['daily']['data'][0]['sunsetTime'])

	
	if sunrise_ts < ts & ts < sunset_ts:
		# based on icon result, return a corresponding image
		return {'pic': w_pic(forecast_info['hourly']['icon'])}
	else:
		# FIX print a result if not daytime in that timezone
		print "it's not daytime"


# create search function 
@app.route('/search', methods=['POST'])
def search():
	# capture the query request from the form into a variable
	question = request.form['query']

	# FIX - way to pull the time from the form or default to the current time - need to add date time
	# as_of = request.form.get('time', datetime.now())

	# query data model file to match name of location to lat & long and then assign to variables
	loc_match = db_session.query(Location).filter(Location.n_hood.ilike("%" + question + "%")).one()
	
	# confirm the infromation captured matches db; otherwise throw error and ask to search again 
	if loc_match:
		# if there is a match the pass to get forecast, validate its day and then get elements to pop results
		forecast_result = validate_day(get_forecast(loc_match))['pic']
		#return redirect(url_for('fast_result'), result=forecast_result)
		return render_template('fast_result.html', result=forecast_result)
	else:
		# FIX using flash or a result on the html page...
		print "Sorry, we are not covering that area at this time. Please try again."
		return redirect(url_for('search'))


	# FIX add image and tempurature to a dictionary that is passed to page

	
# create view that will show simple sun result from search
# @app.route('/fast_result')
# def fast_result():
# 	return render_template('fast_result.html')

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