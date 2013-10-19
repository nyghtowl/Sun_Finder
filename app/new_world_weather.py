from app.models import Location
from config import G_KEY, WUI_KEY
import re # Regex
from datetime import datetime, timedelta
from time import time, mktime
import pytz
import requests, json
from BeautifulSoup import BeautifulSoup

class InputResolver(object):
    def __init__(self, txt_query, user_coord, date):
        self._api_called = False
        self.txt_query = txt_query
        self.user_date = date
        self.user_coord = user_coord

    def fetch_coords(self):
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


    def resolve_location(self):
        # Grabs neighborhood from database 
        # neighborhood = Location.query.filter(Location.n_hood.contains(self.txt_query)).first()

        # # Use local db for coordinates if query matches local db
        # if neighborhood:
        #     self._lat = neighborhood.lat
        #     self._lng = neighborhood.lng
        #     self._location_name = neighborhood.n_hood
        # # Use Google Places for coordinates if no query match to local db
        # else:
        self.fetch_coords()

    @property
    def lat(self):
        return self._lat 

    @property
    def lng(self):
        return self._lng

    @property    
    def location_name(self):
        return self._location_name
    
    @property
    def as_of(self):
        if not(self.user_date):
            return time()
        else:         
            return mktime(datetime.strptime(self.user_date, "%m-%d-%Y").timetuple())

        # tzr = TimezoneResolver(self.user_coord)
        # current_date = tzr.current_dt

        # else:
        #     user_date = datetime.strptime(self.user_date, "%m-%d-%Y")
        #     auto_time = current_date.time()
        #     self.location_dt = datetime.combine(user_date, auto_time)
        #     self.location_dt_str = str(self.location_dt.date())


    # Returns string value if print object
    def __str__(self):
        return ("as_of= " + self.as_of + " lat= " + self.lat + "  lng= " + self.lng + "name " + self.location_name)

class TimezoneResolver(object):
    def __init__(self, user_coord):
        self.user_coord = user_coord
        self._api_called = False
        self.tz_id = None
        self.tz_offset = None

    def fetch_tz_offset(self):
        # Guard - only run once per object
        if self._api_called:
            return
        self._api_called = True

        url = "https://maps.googleapis.com/maps/api/timezone/json?"

# import pdb;pdb.set_trace()
        api_params = {
            'location': self.user_coord,
            'timestamp': time(),
            'sensor':'true'
        }

        tz_result = requests.get(url,params=api_params)
        tz_result_json = tz_result.json()

        self.tz_id = tz_result_json['timeZoneId']

        # Need to convert weather resutls epoch
        self.tz_offset = tz_result_json['dstOffset'] + tz_result_json['rawOffset']

    @property
    def timezone(self):
        self.fetch_tz_offset()
        return pytz.timezone(self.tz_id)

    @property
    def offset(self):
        self.fetch_tz_offset()
        return self.tz_offset

    @property
    def current_dt(self):
        return datetime.fromtimestamp(time(), self.timezone)


# Get sunrise and sunset from earthtools
class DayResolver(object):
    def __init__(self, lat, lng, date):
        self._api_called = False
        self.lat = lat
        self.lng = lng
        self.date = date

    def fetch_sun(self):
        if self._api_called:
            return
        self._api_called = True

        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        earth_final_url=earth_url%(self.lat,self.lng,self.date.day,self.date.month)

        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)

    @property
    def is_day(self):
        sun_position = self.fetch_sun()

        sunrise = datetime.strptime(sun_position.sunrise.string, '%H:%M:%S').time()
        sunset = datetime.strptime(sun_position.sunset.string, '%H:%M:%S').time()
            
        if sunrise < self.date.time() < sunset:
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

    @property
    def weather(self):
        # self._call_api()
        self._build_return_data()
        return self._weather

    # @property
    # def moon(self):
    #     self._call_api()
    #     self._moon

    def _call_api(self):
        if self._called:
            return
        else:
            self._called = True

        url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

        final_url=url%(WUI_KEY, self.lat, self.lng)
        print "weather url", final_url

        self.forecast = requests.get(final_url).json()

    # Store weather data points to post
    def _build_return_data(self):
        self._call_api()
        current = self.forecast['current_observation']
        future = self._pick_future()
        
        if self.current_day:
            self._weather = {
                "icon": current['icon'],
                "temp_F": current['temp_f'],
                "feels_like_F": current['feelslike_f']
            }
        else:
            self._weather = {
                "temp_F": float(future['high']['fahrenheit'])
            }

    def _pick_future(self):
        self.current_day = None
        
        for num, fragment in enumerate(self.forecast['forecast']['simpleforecast']['forecastday']):
            local_ts = float(fragment['date']['epoch']) + self.offset

            # Timestamp offset focus on search location vs location of the server
            forecast_date = datetime.fromtimestamp(local_ts).date() 

            if forecast_date == self.as_of.date():
                print "frament date and num", forecast_date, num
                if num == 0:
                    self.current_day = True

                return fragment

        return None

def choose_picture(is_day, weather, moon_phase):
    pass

class TemplateContext(object):
    pass
