"""
Sun Functions  

"""

from app import db as db_session
from flask import flash
from config import G_KEY
from models import Location, User
import requests # Alt to urllib
import weather_forecast
import re # Regex
from datetime import datetime, timedelta
import dateutil.parser
import time


def google_places_coord(txt_query):
    # Regex to pull space with +
    txt_plus = re.sub('[ ]', '+', txt_query)

    #FIX - Get the client side coord for centralized location
    api_params = {
        # holding central location in SF 
        'query': txt_plus,
        'location':'37.7655, -122.4429',
        'radius':5000,
        'sensor':'false',
        'key':G_KEY
    }

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    result = requests.get(url,params=api_params)
    # Extract lat & lng
    place_result = result.json()
    result_path = place_result['results'][0]['geometry']['location'] 
    g_lat = result_path['lat']
    g_lng = result_path['lng']
   
    if g_lat:
        return (g_lat, g_lng)
    else:
        return None

def search_coord_time(g_lat, g_lng):
    str_lat_lng = str(g_lat) + ',' + str(g_lng)
    today_timestamp = time.time()
    url = "https://maps.googleapis.com/maps/api/timezone/json?"
    
    api_params = {
        'location':str_lat_lng,
        'timestamp':today_timestamp,
        'sensor':'true'
    }

    result = requests.get(url,params=api_params)
    result_json = result.json()
    return (today_timestamp, today_timestamp + result_json['dstOffset'] + result_json['rawOffset'])

# Generate valid as_of date to create weather object
def extract_as_of(user_picked_time_str, utc_timestamp, today_timestamp):
    # auto_date = dateutil.parser.parse(auto_date_str, ignoretz=True)

    print 'timestamp', today_timestamp, utc_timestamp
    today_datetime = datetime.fromtimestamp(today_timestamp)

    print 'dt timestamp', today_datetime

    if not(user_picked_time_str):
        as_of = today_datetime
    else:
        # Adds automatically generated time to entered date
        # FIX - allow to change if allowing time choice
        as_of_date = datetime.strptime(user_picked_time, "%m-%d-%Y")
        # Applies auto time to the date picked / not timepicker
        as_of_time = today_datetime.time() 
        as_of = datetime.combine(as_of_date,as_of_time)

    print 'as of', as_of

    return (as_of, today_datetime)

# Get weather data
def search_results(txt_query, user_picked_time):
    loc_name = None

    # Grabs neighborhood from database 
    neighborhood = Location.query.filter(Location.n_hood.contains(txt_query)).first()

    # Use local db for coordinates if query matches local db
    if neighborhood:
        g_lat = neighborhood.lat
        g_lng = neighborhood.lng
        loc_name = neighborhood.n_hood
    # Use Google Places for coordinates if no query match to local db
    else:
        g_lat, g_lng = google_places_coord(txt_query)

    utc_timestamp, today_timestamp = search_coord_time(g_lat, g_lng)
    
    # Format date to datetime
    as_of, today_time = extract_as_of(user_picked_time, utc_timestamp, today_timestamp)

    if not g_lat:
        flash("%s not found. Please try your search again." % txt_query, category="error")
 
    forecast_result = weather_forecast.Weather.get_forecast(g_lat, g_lng, as_of, today_time)

    # Confirm time of day to figure out picture to apply
    forecast_result.apply_pic()
    
    # Applies neighborhood name if from local db
    if loc_name:
        forecast_result.add_name(loc_name) 

    # Return weather data
    return forecast_result

