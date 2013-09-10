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


def get_coord(txt_query, as_of):
    # Regex to pull space with +
    txt_plus = re.sub('[ ]', '+', txt_query)

    # params option not working because location pass is lat,lng - is there a fix?
    # api_params = {
    #     # holding central location in SF and 
    #     'query':txt_plus,
    #     'location':'37.7655, -122.4429',
    #     'radius':5000,
    #     'sensor':'false',
    #     'key':G_KEY
    # }

    # url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    # result = requests.get(url,params=api_params)

    central_lat = 37.7655
    central_lng = -122.4429
    central_rad = 5000

    # Google Places api url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&location=%f,%f&radius=%f&sensor=%s&key=%s"
    
    # FIX change when ready to cover all bay area #central_rad = 8000

    # Results from Google Places
    final_url = url % (txt_plus, central_lat, central_lng, central_rad, 'false', G_KEY)
    response = requests.get(final_url)
    
    print final_url # Review

    # Revise response to json, and seperate out the lat and long
    place_result = response.json()
    result_path = place_result['results'][0]['geometry']['location'] 
    g_lat = result_path['lat']
    g_lng = result_path['lng']
   
    print g_lat, g_lng # Review

    # Return Weather object if coordinates exist
    if g_lat:
        return weather_forecast.Weather.get_forecast(g_lat, g_lng, as_of)
    else:
        flash("%s not found. Please try your search again." % (txt_query, as_of), category="error")
        return None


# Validate the date chosen for search has data results
def validate_date(as_of):
    if as_of.date() < datetime.now().date():
        return False
    if as_of.date() > (datetime.now() + timedelta(days=7)).date():
        return False
    return True

# Generate valid as_of date to create weather object
def extract_as_of(manual_date_str, auto_date_str):
    # auto_date_str example format: Thu Sep 05 2013 21:47:00 GMT-0700 (PDT)
    auto_date = dateutil.parser.parse(auto_date_str, ignoretz=True)
    print 101, auto_date.date()

    if not(manual_date_str):
        as_of = auto_date

    else:
        # Adds automatically generated time to entered date
        # FIX - allow to change if allowing time choice
        as_of_date = datetime.strptime(manual_date_str, "%Y-%m-%d")
        as_of_time = auto_date.time() # Applies a auto time to the date picked / not timepicker
        as_of = datetime.combine(as_of_date,as_of_time)
        print 102, as_of

    # Fall back to current for bad date
    if not validate_date(as_of):
        flash("FAILED: %s date unsupported, today's date used instead." % as_of, category="error")
        as_of = auto_date

    return as_of 

# Search results
def search_results(locations, manual_date, auto_date, txt_query):

    g_lat = g_lng = None

    # Format date to datetime
    as_of = extract_as_of(manual_date, auto_date)
    
    # FIX - search by specif time
    # Pull time from client
    # If date entered on client, only take auto time capture other take all
    # Convert returned data to utc and combine data and time if entered separately
    # Pass date and time through the function to determine image to show
    # Return date time to page results

    # Use local db for coordinates if query matches local db
    for location in locations:
        if location.n_hood == txt_query:
            g_lat = location.lat
            g_lng = location.lng
            loc_name = location.n_hood
    if g_lat:
        forecast_result = weather_forecast.Weather.get_forecast(g_lat, g_lng, as_of)
        forecast_result.add_name(loc_name) # Applies neighborhood name if from local db
    # Use Google Places for coordinates if no query match to local db
    else:
        forecast_result = get_coord(txt_query, as_of)

    # Validate time of date to determine picture to assign
    forecast_result.apply_pic()

    # Return forecast result
    return forecast_result


