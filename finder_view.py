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
	Finish linking up date
	How to load/reference Javascript from js doc
	Build out autocomplete w/ Liz direction
	Put text and links on map
	Setup map to pop-up on first page and allow selection of neighborhood for autocomplete


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
	central_lat = 37.7655
	central_lng = -122.4429
	central_rad = 5000

	#change when ready to cover all bay area #central_rad = 8000

	# request results from Google Places
	final_url = url % (txt_plus, central_lat, central_lng, central_rad, 'false', G_KEY)
	response = requests.get(final_url)

	# revise response to json, and seperate out the lat and long
	place_result = response.json()
	g_lat = place_result['results'][0]['geometry']['location']['lat']
	g_lng = place_result['results'][0]['geometry']['location']['lng']
	print g_lat, g_lng

	# return dictionary of coordinates
	return {'lat':g_lat, 'lng':g_lng}


def get_forecast(lat, lon):
	# url to pass to Forecast.io
    fio_url="https://api.forecast.io/forecast/%s/%f,%f"
	# pull API key from env with FIO_KEY
    fio_final_url=fio_url%(FIO_KEY, lat,lon)
    print fio_final_url
    fio_response = requests.get(fio_final_url).json()

	# url to pass to WUI
    wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"
	# pull API key from env with FIO_KEY
    wui_final_url=wui_url%(WUI_KEY, lat,lon)
    print wui_final_url
    wui_response = requests.get(wui_final_url).json()

    fio_rise = fio_response['daily']['data'][0]['sunriseTime']
    fio_set = fio_response['daily']['data'][0]['sunsetTime']

    sunrise = datetime.datetime.utcfromtimestamp(fio_rise)
    sunset = datetime.datetime.utcfromtimestamp(fio_set)

    # generated a dictionary of forecast data points pulling from both weather sources
    return {
    	'icon': fio_response['hourly']['icon'],
    	'tempr_wui_F': wui_response['current_observation']['temp_f'],
    	'tempr_wui_C': wui_response['current_observation']['temp_c'],
    	'tempr_wui_str': wui_response['current_observation']['temperature_string'],
    	'tempr_fio_F':fio_response['currently']['temperature'], 
    	'cloud_cover':fio_response['currently']['cloudCover'],
    	'loc_name': '', # FIX pull name from ?
    	'time':time.time(),
    	'sunrise':fio_rise,
    	'sunset':fio_set,
    	'wind_gust_mph': wui_response['current_observation']['wind_gust_mph'],
    	'feels_like_str': wui_response['current_observation']['feelslike_string'],
    	'feels_like_F': wui_response['current_observation']['feelslike_f'],
    	'feels_like_C': wui_response['current_observation']['feelslike_c'],
    	'mult_day': wui_response['forecast']['simpleforecast']['forecastday']
    	}
    
# FIX - write function to give human results to wind speed - e.g. dress wearing, difficult to walk

# convert icon result to an image
def add_pic(icon, cloud):
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
	
	# FIX how to handle wind icon result and night 

	if icon in weather_pics:
		# forces clear day result if the cloud cover is < 20%
		if (icon == 'partly-cloudy-day') & (cloud < .20):
			return pic_location + weather_pics['clear-day']	
		else:
			#print weather_pics[icon]
			final_pic_loc = pic_location + weather_pics[icon]
			return final_pic_loc

	#FIX - what happends if not result
		
# pulls forecast information from work on incorporating as_of
def validate_day(forecast_dict, as_of=None):
	
	# FIX as_of and how to pull out results that are not current date

	print forecast_dict['icon']
	print as_of
	ts = time.time()

	# get actual time and compare on whether it is date
	sunrise_ts = forecast_dict['sunrise']
	sunset_ts = forecast_dict['sunset']
	print sunrise_ts
	print sunset_ts

	# condition to only show sun in the daytime based on sunrise and sunset
	if sunrise_ts < ts < sunset_ts:
		forecast_dict['pic'] = add_pic(forecast_dict['icon'], forecast_dict['cloud_cover'])
	else:

		# FIX print a result if not daytime in that timezone
		
		print "it's not daytime"
		forecast_dict['pic'] = None

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
		as_of = datetime.datetime.strptime(date_query, "%Y-%m-%d")
	
	print as_of

	# FIX - datetime.datetime.utcfromtimestamp(timestamp) - to conver timestamps from fio
	# FIX - datetime.datetime.strptime(..., "%m/%d/%Y") ?
	
	# pull coordinates from Google Places
	coord_result = get_coord(txt_query)
	
	#FIX - push certain results back to Google Places to improve weigh results for neighborhoods & potentially still use local db on neighborhoods

	# validate there are coordinates and then get the forecast
	if coord_result:
		forecast_result = get_forecast(coord_result['lat'],coord_result['lng'])
		validate_day(forecast_result, as_of)
		#x_test = validate_day_test(get_forecast_test(coord_result['lat'],coord_result['lng']))

		# FIX the name that is used to come from query results

		forecast_result['loc_name'] = txt_query.title()
		session['forecast'] = forecast_result
		session['test'] = 'hi'
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
	#forecast_details = session['forecast']
	test2 = session.get('test')
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