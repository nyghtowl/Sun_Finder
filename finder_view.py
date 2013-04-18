"""
finder_view.py -- A flask based sun search tool

TO DO: 
	Go Live: 
		change secret key 
		turn off debug

	Currently small sample used and picking center of neighborhood. Future would be good to find a better way to apply

QUESITONS / ERROR:
	check about how the seed file is linked to model file - how it calls it when it runs
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

# capture forecast from forecast.io
def forecast(lat,lon):
    url="https://api.forecast.io/forecast/%s/%f,%f"
	# pull API key from env with FIO_KEY
    final_url=url%(FIO_KEY, lat,lon)
    print final_url
    response = requests.get(final_url)
    return response.json()

# convert icon result to an image
def weather_pic(icon):
	pic_location = "/static/img/"
	# holds weather images for reference
	weather_pics = {"clear-day":"sun_samp2.jpeg", "rain":"rain.png" , "snow":"snow.png", "sleet":"sleet2.png", "fog":"foggy2.png" , "cloudy":"cloudy.png", "partly-cloudy-day":"partly_cloudy.png"}
	
	#print weather_pics["clear-day"]
	# FIX how to handle wind icon result - determine percent cloud cover? and 
	if icon in weather_pics:
		#print weather_pics[icon]
		final_pic_loc = pic_location + weather_pics[icon]
		print final_pic_loc
	
#	print type(icon)
	return final_pic_loc

# create actual search function to enter the name of the location
@app.route('/search', methods=['POST'])
def search():
	# capture the query request from the form into a variable
	question = request.form['query']

	# query data model file to match name of location to lat & long and then assign to variables
	loc_match = db_session.query(Location).filter(Location.n_hood.ilike("%" + question + "%")).one()
	
	# confirm the infromation captured matches db; otherwise throw error and ask to search again 
	if loc_match:
		lat = loc_match.lati
		lon = loc_match.longi
		# submit lat, long and api key and store json/dicationary result into variable
		forecast_result = forecast(lat, lon)
		print forecast_result['hourly']['icon']
		# return the results template
		icon_result = weather_pic(forecast_result['hourly']['icon']) 
		
		#return redirect(url_for('fast_result'), result=forecast_result)
		return render_template('fast_result.html', result=icon_result)
	else:
		print "Sorry, we are not covering that area at this time. Please try again."
		return redirect(url_for('search'))


	# parse json result and pull icon and tempurature data and assign to variables

	# based on icon result, return a corresponding image

	# print image and tempurature data on page

	

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