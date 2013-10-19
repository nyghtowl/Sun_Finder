from sun_functions import google_places_coord
from datetime import datetime, timedelta
import pytz
from BeautifulSoup import BeautifulSoup
from time import time
import requests, json

class InputResolver(object):
    def __init__(self, query, user_coord, date):
        self.query = query
        self.user_date = date
        self.user_coord = user_coord
        self.lat = None
        self.lng = None
        self.location_name = None
        self.location_dt = None

    # FIX - only run if not in postgres
    def resolve_location(self):
        # FIX - remove lat and lng? - pull in google api
        self.lat, self.lng, self.location_name = google_places_coord(self.query, self.user_coord)

    def set_date(self): 
        tzr = TimezoneResolver(self.user_coord)
        current_date = tzr.current_dt

        if not(self.user_date):
            self.location_dt = current_date
        else:
            user_date = datetime.strptime(self.user_date, "%m-%d-%Y")
            auto_time = current_date.time()
            self.location_dt = datetime.combine(user_date, auto_time)
            self.location_dt_str = str(self.location_dt.date())


    # Returns string value if print object
    def __str__(self):
        return ("query= " + self.query + " user_coord= " + self.user_coord + "  name= " + self.location_name)

class TimezoneResolver(object):
    def __init__(self, user_coord):
        self.user_coord = user_coord
        self._api_called = False
        self.tz_id = None
        self.tz_offset = None

    def fetch_tz_offset(self):
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
        self.lat = lat
        self.lng = lng
        self.date = date
        self.is_day = None

    def earthtools_sun_info(self):
        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        earth_final_url=earth_url%(self.lat,self.lng,self.date.day,self.date.month)

        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)

    def get_is_day(self):
        sun_position = self.earthtools_sun_info()

        sunrise = datetime.strptime(sun_position.sunrise.string, '%H:%M:%S').time()
        sunset = datetime.strptime(sun_position.sunset.string, '%H:%M:%S').time()
            
        if sunrise < self.date.time() < sunset:
            self.is_day = True
        else:
            self.is_day = False

class WeatherFetcher(object):
    def __init__(self, lat, lng, date):
        self._called = False
        self.lat = lat
        self.lng = lng
        self.date = date

    # @property
    # def weather(self):
    #     self._call_api()
    #     self._weather

    # @property
    # def moon(self):
    #     self._call_api()
    #     self._moon

    def _call_api():
        pass
        # if self._called:
        #     return
        # else:
        #     self._called = True
        # # Url to pass to WUI 
        # wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

        # # Pull API key from env with FIO_KEY
        # wui_final_url=wui_url%(WUI_KEY, lat, lng)
        # print "weather underground url", wui_final_url

        # wui_response = requests.get(wui_final_url).json()

        # # Generated a dictionary of forecast data points pulling from both weather sources
        # current = wui_response['current_observation']
        # future = self._pick_future(self.desired_date)
        # self._weather = {
        # "icon": current['icon'],
        # "feels_like_F": current['feelslike_f'],...

        # }
        # if future:
        #     self._weather.update({
        #         'high_F': future['high']['fahrenheit'],
        #         ...
        #     })

def choose_picture(is_day, weather, moon_phase):
    pass

class TemplateContext(object):
    pass
