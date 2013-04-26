"""
sun_functions.py -  Sun Finder functions  

"""
# use requests to pull information from api requests - alternative is urllib - this is more human
import requests
import weather_forecast
# utilize for regular expressions
import re

def get_coord(txt_query, G_KEY, FIO_KEY, WUI_KEY):
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
	result_path = place_result['results'][0]['geometry']['location'] 
	g_lat = result_path['lat']
	g_lng = result_path['lng']
	print g_lat, g_lng

	# return Weather object if coordinates exist
	if g_lat:
		return weather_forecast.Weather.get_forecast(g_lat, g_lng, FIO_KEY, WUI_KEY)
	else:
		return None
