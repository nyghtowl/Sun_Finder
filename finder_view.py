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
# utilize for regular expressions
import re

# initialize program to be a Flask app and set a key to keep client side session secure
app = Flask(__name__)
app.secret_key = 'key'

app.config.from_object(__name__) # allows for setting all caps var as global var
# eg: SECRET_KEY = "bbbb"

# pull api keys from environment
FIO_KEY = os.environ.get('FIO_KEY')
G_KEY = os.environ.get('G_KEY')
WUI_KEY = os.environ.get('WUI_KEY')

@app.route('/')
def index():
	return redirect(url_for('search'))

# Display search // potentially this is the index page and just redirect
@app.route('/search')
def display_search():
	return render_template('search.html')


def get_coord(txt_query):
	# use regex to swap space with plus and add neighborhood to help focus results
	txt_plus = re.sub('[ ]', '+', txt_query) + '+neighborhood'

	# url to pass to Google Places api
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&location=%f,%f&radius=%f&sensor=%s&key=%s"
	
	# holding central location in SF and 
	central_lat = 37.7697
	central_lng = -122.4781
	central_rad = 10

	# request results from Google Places
	final_url = url % (txt_plus, central_lat, central_lng, central_rad, 'false', G_KEY)
	print final_url
	response = requests.get(final_url)

	# revise response to json, and seperate out the lat and long
	place_result = response.json()
	g_lat = place_result['results'][0]['geometry']['location']['lat']
	g_lng = place_result['results'][0]['geometry']['location']['lng']
	print g_lat, g_lng

	# return dictionary of coordinates
	return {'lat':g_lat, 'lng':g_lng}

# submit lat, long and api key and store json/dicationary result into variable
#def get_forecast_org(location):
	# lat = location.lati
 #    lon = location.longi
 #    url="https://api.forecast.io/forecast/%s/%f,%f"
	# final_url=url%(FIO_KEY, lat,lon)
 #    print final_url
 #    response = requests.get(final_url)
 #    return response.json()

def get_forecast(lat, lon):
	# url to pass to Forecast.io
    url="https://api.forecast.io/forecast/%s/%f,%f"
	# pull API key from env with FIO_KEY
    final_url=url%(FIO_KEY, lat,lon)
    print final_url
    response = requests.get(final_url)
    return response.json()

# convert icon result to an image
def w_pic(icon, cloud):
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
		# forces clear day result if the cloud cover is < 20%
		if (icon == 'partly-cloudy-day') & (cloud < .20):
			return pic_location + weather_pics['clear-day']	
		else:
			#print weather_pics[icon]
			final_pic_loc = pic_location + weather_pics[icon]
			print final_pic_loc
			return final_pic_loc
	#FIX - what happends if not result

		
# pulls forecast information from work on incorporating as_of
def validate_day(forecast_info):
	
	print forecast_info['hourly']['icon']
	
	# get actual time and compare on whether it is day
	ts = int(time.time())
	sunrise_ts = int(forecast_info['daily']['data'][0]['sunriseTime'])
	sunset_ts = int(forecast_info['daily']['data'][0]['sunsetTime'])

	# pull cloud cover value to help determine what image to return
	per_cloud = forecast_info['currently']['cloudCover']
	print per_cloud

	# condition to only show sun in the daytime based on sunrise and sunset
	if sunrise_ts < ts & ts < sunset_ts:
		return {'pic': w_pic(forecast_info['hourly']['icon'], per_cloud), 'tempr': forecast_info['currently']['temperature'], 'loc_name': None, 'forecast':forecast_info}
	else:

		# FIX print a result if not daytime in that timezone
		
		print "it's not daytime"
		return {'pic': None, 'tempr': None, 'loc_name': None}


# create search function 
@app.route('/search', methods=['POST'])
def search():
	# capture the query request from the form into a variable
	txt_query = request.form['query']

	# FIX - way to pull the time from the form or default to the current time - need to add date time
		# as_of = request.form.get('time', datetime.now())

	# pull coordinates from Google Places
	coord_result = get_coord(txt_query)
	
	#FIX - push certain results back to Google Places to improve weigh results for neighborhoods & potentially still use local db on neighborhoods

	if coord_result:
		forecast_result = validate_day(get_forecast(coord_result['lat'],coord_result['lng']))
		
		# FIX the name that is used to come from query results

		forecast_result['loc_name'] = txt_query.title()
		return render_template('fast_result.html', result = forecast_result)
	
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

# FIX - not working yet because need to figure out how to pass forecast	
# create extended view that of weather results
@app.route('/more_details/')
def more_details(forecast=None):
	#loc_details = forecast['forecast']
	print forecast
 	#return render_template('more_details.html' details=loc_details)

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