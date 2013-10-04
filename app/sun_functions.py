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
from datetime import datetime
import json

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
    result_path = place_result['results'][0] 
    g_lat = result_path['geometry']['location']['lat']
    g_lng = result_path['geometry']['location']['lng']
    loc_name = result_path['name']
   
    if g_lat:
        return (g_lat, g_lng, loc_name)
    else:
        return None

def daily_weather_report(locations):

    daily_weather = []

    for location in locations:
        if redis_db.exists((location.lat, location.lng)):
            nh_weather_str = redis_db.get((location.lat, location.lng))
            nh_weather_dict = json.loads(nh_weather_str)
            daily_weather.append(nh_weather_dict)
    print "daily_weather in sun functions"
    return daily_weather

# Get weather data
def search_results(txt_query, user_picked_time, user_coord):

    # Grabs neighborhood from database 
    neighborhood = Location.query.filter(Location.n_hood.contains(txt_query)).first()

    # Use local db for coordinates if query matches local db
    if neighborhood:
        g_lat = neighborhood.lat
        g_lng = neighborhood.lng
        loc_name = neighborhood.n_hood
    # Use Google Places for coordinates if no query match to local db
    else:
        g_lat, g_lng, loc_name = google_places_coord(txt_query, user_coord)

    if not g_lat:
        flash("%s not found. Please try your search again." % txt_query, category="error")
 
    forecast_result = weather_forecast.Weather.get_forecast(g_lat, g_lng, user_picked_time, loc_name)
    
    # Return weather data
    return forecast_result

