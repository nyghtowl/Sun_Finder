from app.models import Location
from config import G_KEY, WUI_KEY
import re # Regex
from datetime import datetime, timedelta, date
from time import time, mktime
import pytz
import moonphase
import requests, json
from BeautifulSoup import BeautifulSoup

class InputResolver(object):
    def __init__(self, txt_query, user_coord, date):
        self._api_called = False
        self._loc_resolve = False
        self.txt_query = txt_query
        self.user_date = date
        self.user_coord = user_coord

    def _fetch_coords(self):
        if self._api_called:
            return
        self._api_called = True

        # Regex to pull space with +
        txt_plus = re.sub('[ ]', '+', self.txt_query)

        #FIX - Get the client side coord for centralized location
        api_params = {
            # holding central location in SF 
            'query': txt_plus,
            'location': self.user_coord,
            'radius':5000,
            'sensor':'false',
            'key':G_KEY
        }

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        result = requests.get(url,params=api_params)
        # Extract lat & lng
        place_result = result.json()
        result_path = place_result['results'][0] 

        self._lat = result_path['geometry']['location']['lat']
        self._lng = result_path['geometry']['location']['lng']
        self._location_name = result_path['name']

    def _resolve_location(self):
        if self._loc_resolve:
            return
        self._loc_resolve = True

        # Grabs neighborhood from database 
        neighborhood = Location.query.filter(Location.n_hood.contains(self.txt_query)).first()

        # Use local db for coordinates if query matches local db
        if neighborhood:
            self._lat = neighborhood.lat
            self._lng = neighborhood.lng
            self._location_name = neighborhood.n_hood
        # Use Google Places for coordinates if no query match to local db
        else:
            self._fetch_coords()

    @property
    def lat(self):
        self._resolve_location()
        return self._lat 

    @property
    def lng(self):
        self._resolve_location()
        return self._lng

    @property    
    def location_name(self):
        self._resolve_location()
        return self._location_name
    
    @property
    def as_of_ts(self):
        if not(self.user_date):
            return time() 
        else:         
            #Added time at the time of search into the timestamp
            add_time = str(datetime.utcnow().hour) + ":" + str(datetime.utcnow().minute)
            self.user_date += " " + add_time

            return mktime(datetime.strptime(self.user_date, "%m-%d-%Y %H:%M").timetuple())

    # Returns string value if print object
    def __str__(self):
        return ("as_of= " + self.as_of + " lat= " + self.lat + "  lng= " + self.lng + "name " + self.location_name)

class TimezoneResolver(object):
    def __init__(self, user_coord):
        self.user_coord = user_coord
        self._api_called = False

    def _fetch_timezone(self):
        # Guard - only run once per object
        if self._api_called:
            return
        self._api_called = True

        url = "https://maps.googleapis.com/maps/api/timezone/json?"

        api_params = {
            'location': self.user_coord,
            'timestamp': time(),
            'sensor':'true'
        }

        tz_result = requests.get(url,params=api_params)
        tz_result_json = tz_result.json()

        self._id = tz_result_json['timeZoneId']

        # Need to convert weather resutls epoch
        self._offset = tz_result_json['dstOffset'] + tz_result_json['rawOffset']

    @property
    def timezone(self):
        self._fetch_timezone()
        return pytz.timezone(self._id)

    @property
    def offset(self):
        self._fetch_timezone()
        return self._offset


# Get sunrise and sunset from earthtools
class DayResolver(object):
    def __init__(self, lat, lng, as_of_ts, offset):
        self._api_called = False
        self.lat = lat
        self.lng = lng
        self.as_of_ts = as_of_ts
        self.offset = offset

    def _fetch_sun(self):
        if self._api_called:
            return
        self._api_called = True
        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        earth_final_url=earth_url%(self.lat,self.lng,self.as_of_dt.day,self.as_of_dt.month)
        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)
    
    @property
    def as_of_dt(self):
        return datetime.utcfromtimestamp(self.as_of_ts + self.offset)

    @property
    def is_day(self):
        sun_position = self._fetch_sun() #local time

        sunrise = datetime.strptime(sun_position.sunrise.string, '%H:%M:%S').time()
        sunset = datetime.strptime(sun_position.sunset.string, '%H:%M:%S').time()
            
        if sunrise < self.as_of_dt.time() < sunset:
            return True
        else:
            return False

class WeatherFetcher(object):
    def __init__(self, lat, lng, as_of, offset):
        self._called = False
        self.lat = lat
        self.lng = lng
        self.as_of = as_of
        self.offset = offset
        self.current_day = None

    @property
    def weather(self):
        # self._call_api()
        self._weather_data()
        return self._weather

    @property
    def moon(self):
        return moonphase.main(self.as_of)

    def _call_api(self):
        if self._called:
            return
        else:
            self._called = True

        url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

        final_url=url%(WUI_KEY, self.lat, self.lng)

        self.forecast = requests.get(final_url).json()

    # Store weather data points to post
    def _weather_data(self):
        self._call_api()
        current = self.forecast['current_observation']
        chosen_day, is_current = self._find_day()
        
        common_weather = {
            "humidty": chosen_day['avehumidity'],
            "high_F": chosen_day['high']['fahrenheit'],
            "high_C": chosen_day['high']['celsius'],
            "low_F": chosen_day['low']['fahrenheit'],
            "low_C": chosen_day['low']['celsius'],
        }
        
        if is_current:
            self._weather = {
                "icon": current['icon'],
                "temp_F": current['temp_f'],
                "temp_C": current['temp_c'],
                "feels_like_F": current['feelslike_f'],
                "feels_like_C": current['feelslike_f'],
                "wind_gust_mph": current['wind_gust_mph'],
            }
        else:
            self._weather = {
                "icon": chosen_day['icon'],
                "temp_F": float(chosen_day['high']['fahrenheit']),
                "temp_C": float(chosen_day['high']['celsius']),
                "feels_like_F": None,
                "feels_like_C": None,
                "wind_gust_mph": chosen_day['avewind']['mph'],
            }
        self._weather.update(common_weather)

    def _find_day(self):

        for num, fragment in enumerate(self.forecast['forecast']['simpleforecast']['forecastday']):
            local_ts = float(fragment['date']['epoch']) + self.offset

            # Timestamp offset focus on search location vs location of the server
            forecast_date = datetime.fromtimestamp(local_ts).date() 

            if forecast_date == self.as_of.date():
                if num == 0:
                    is_current = True
                else:
                    is_current = False

                return fragment, is_current

        return None, False


def choose_picture(icon, moon_phase, is_day):    
    
    day_pics = {
        "clear-day":("sun", "sun_samp2.png"),
        "clear":("sun", "sun_samp2.png"),
        "rain":("rain", "rain.png"), 
        "snow":("snow", "snow.png"), 
        "sleet":("sleet", "sleet2.png"), 
        "fog":("fog", "foggy2.png"), 
        "cloudy":("cloudy", "cloudy.png"), 
        "mostlycloudy":("partly cloudy", "cloudy.png"),
        "partlycloudy":("partly cloudy", "partly_cloudy.png")
    }

    night_pics = {
        "First Quarter":("First Quarter Moon","moon_firstquarter.png"), 
        "Full Moon":("Full Moon","full_moon1.jpg"), 
        "Last Quarter":("Last Quarter Moon","moon_lastquarter.png"), 
        "New Moon":("New Moon","newmoon.png"), 
        "Waning Crescent":("Waning Crescent Moon","moon_waningcrescent.png"),
        "Waning Gibbous":("Waning Gibbous Moon","moon_waninggibbous.png"), 
        "Waxing Crescent":("Waxing Crescent Moon","moon_waxingcrescent.png"), 
        "Waxing Gibbous":("Waxing Gibbous Moon","moon_waxinggibbous.png")
        }

    if is_day:
        return day_pics[icon]
    else:
        return night_pics[moonphase]


