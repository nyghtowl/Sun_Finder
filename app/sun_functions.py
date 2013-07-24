"""
sun_functions.py -  Sun Finder functions  

"""

from app import db as db_session
# import model and assign to db_session variable
from models import Location, User
# use requests to pull api info - alternative is urllib - this is more human
import requests
import weather_forecast
# utilize for regular expressions
import re
# leverage for reporting time result
from datetime import datetime, timedelta
import time


def get_coord(txt_query, G_KEY, FIO_KEY, WUI_KEY, as_of):
    # use regex to swap space with plus and add neighborhood to help focus results
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

    # url to pass to Google Places api
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&location=%f,%f&radius=%f&sensor=%s&key=%s"
    
    #change when ready to cover all bay area #central_rad = 8000

    # request results from Google Places
    final_url = url % (txt_plus, central_lat, central_lng, central_rad, 'false', G_KEY)
    response = requests.get(final_url)
    
    print final_url #test

    # revise response to json, and seperate out the lat and long
    place_result = response.json()
    result_path = place_result['results'][0]['geometry']['location'] 
    g_lat = result_path['lat']
    g_lng = result_path['lng']
   
    print g_lat, g_lng # test

    # return Weather object if coordinates exist
    if g_lat:
        return weather_forecast.Weather.get_forecast(g_lat, g_lng, FIO_KEY, WUI_KEY, as_of)
    else:
        return None

        #FIX flash a message to try search again if coord_result is not valid


# validate the date chosen for search has data results
def validate_date(as_of):
    if as_of.date() < datetime.now().date():
        return False
    if as_of.date() > (datetime.now() + timedelta(days=7)).date():
        return False
    return True

# generate valid as_of date to create weather object
def extract_as_of(date_string):
    if not(date_string):
        as_of = datetime.now()
    else:
        #grabs date that is entered and combines with automatically generated time
        as_of_date = datetime.strptime(date_string, "%Y-%m-%d")
        as_of_time = datetime.now().time() #this applies a auto time to the date picked / not timepicker
        as_of = datetime.combine(as_of_date,as_of_time)

    if not validate_date(as_of):
        # fall back to current for bad date
        # TODO: flash an error instead?
        print "FAILED date unsupported %s" % as_of
        as_of = datetime.now()

    return as_of 

# function to generate search results for the different views
def search_results(G_KEY, FIO_KEY, WUI_KEY, locations, date, txt_query):

    g_lat = None
    g_lng = None

    # determine date captured to utilize
    as_of = extract_as_of(date)
    
    # FIX - search by specif time

    # utilize local db for coordinates if query relates
    for location in locations:
        if location.n_hood == txt_query:
            g_lat = location.lat
            g_lng = location.lng
            loc_name = location.n_hood
    if g_lat:
        forecast_result = weather_forecast.Weather.get_forecast(g_lat, g_lng, FIO_KEY, WUI_KEY, as_of)
        forecast_result.add_name(loc_name) # applies neighborhood name if from local db
    # if no query match to local db use Google Places
    else:
        forecast_result = get_coord(txt_query, G_KEY, FIO_KEY, WUI_KEY, as_of)

    # validate time of date to determine picture to assign
    forecast_result.apply_pic()

    # returns forecast result
    return forecast_result


    #FIX flash a message to try search again if coord_result is not valid

