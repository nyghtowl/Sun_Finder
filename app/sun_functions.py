"""
Sun Functions  

"""

from app import db as db_session, redis_db
from flask import flash
from config import G_KEY
from models import Location, User
import requests # Alt to urllib
import weather_forecast
import re # Regex
from datetime import datetime, timedelta
import time, json
from pytz import timezone


def google_places_coord(txt_query, user_coord):
    # Regex to pull space with +
    txt_plus = re.sub('[ ]', '+', txt_query)

    #FIX - Get the client side coord for centralized location
    api_params = {
        # holding central location in SF 
        'query': txt_plus,
        'location': user_coord,
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

def search_coord_timezone(g_lat, g_lng, utctimestamp):
    str_lat_lng = str(g_lat) + ',' + str(g_lng)
    url = "https://maps.googleapis.com/maps/api/timezone/json?"
    
    api_params = {
        'location':str_lat_lng,
        'timestamp':utctimestamp,
        'sensor':'true'
    }

    result = requests.get(url,params=api_params)
    result_json = result.json()
    return result_json['timeZoneId']

# Generate valid as_of date to create weather object
def extract_as_of(user_picked_time_str, utc_timestamp, timezone_id):
    local_tz = timezone(timezone_id)
    print 'timestamp', utc_timestamp
    current_local_time = datetime.fromtimestamp(utc_timestamp, local_tz)

    if not(user_picked_time_str):
        as_of = current_local_time
    else:
        # Adds automatically generated time to entered date
        # FIX - allow to change if allowing time choice
        as_of_date = datetime.strptime(user_picked_time_str, "%m-%d-%Y")
        # Applies auto time to the date picked / not timepicker
        as_of_time = current_local_time.time() 
        as_of = datetime.combine(as_of_date,as_of_time)

    print 'as of', as_of

    return (as_of, current_local_time, local_tz)

def daily_weather_report(locations):

    daily_weather = []

    for location in locations:
        if redis_db.exists((location.lat, location.lng)):
            nh_weather_str = redis_db.get((location.lat, location.lng))
            nh_weather_dict = json.loads(nh_weather_str)
            daily_weather.append(nh_weather_dict)
    print "list for map ", daily_weather
    print daily_weather[1]['img_url']
    return daily_weather

# Get weather data
def search_results(txt_query, user_picked_time, user_coord):
    loc_name = None
    utctimestamp = time.time()

    # Grabs neighborhood from database 
    neighborhood = Location.query.filter(Location.n_hood.contains(txt_query)).first()

    # Use local db for coordinates if query matches local db
    if neighborhood:
        g_lat = neighborhood.lat
        g_lng = neighborhood.lng
        loc_name = neighborhood.n_hood
    # Use Google Places for coordinates if no query match to local db
    else:
        g_lat, g_lng = google_places_coord(txt_query, user_coord)

    timezone_id = search_coord_timezone(g_lat, g_lng, utctimestamp)
    
    # Format date to datetime
    as_of, current_local_time, local_tz = extract_as_of(user_picked_time, utctimestamp, timezone_id)

    if not g_lat:
        flash("%s not found. Please try your search again." % txt_query, category="error")
 
    forecast_result = weather_forecast.Weather.get_forecast(g_lat, g_lng, as_of, current_local_time)

    # Confirm time of day to figure out picture to apply
    forecast_result.apply_pic(local_tz)
    
    # Applies neighborhood name if from local db
    if loc_name:
        forecast_result.add_name(loc_name) 

    # Return weather data
    return forecast_result

