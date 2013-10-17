from sun_functions import google_places_coord
from datetime import datetime, timedelta
from pytz import timezone
from BeautifulSoup import BeautifulSoup
import time, requests, json

class InputResolver(object):
    def __init__(self, query, user_coord, date):
        self.query = query
        self.user_date = date
        self.user_coord = user_coord

    # FIX - only run if not in postgres
    def get_name(self):
        # FIX - remove lat and lng? - pull in google api
        self.lat, self.lng, self.location_name = google_places_coord(self.query, self.user_coord)

    def set_date(self): 
        set_dt = TimezoneResolver(self.user_coord)
        set_dt.set_current_dt()

        if not(self.user_date):
            self.location_dt = set_dt.current_dt
        else:
            user_date = datetime.strptime(self.user_date, "%m-%d-%Y")
            auto_time = set_dt.current_dt.time()
            self.location_dt = datetime.combine(user_date, auto_time)
            self.location_dt_str = str(self.location_dt.date())


    # Returns string value if print object
    def __str__(self):
        return ("query= " + self.query + " user_coord= " + self.user_coord + "  name= " + self.location_name)

class TimezoneResolver(object):
    def __init__(self, user_coord):
        self.utc_stamp = time.time()
        self.user_coord = user_coord
        self.tz_id = None
        self.tz_offset = None
        self.dt_tz_id = None

    def get_tz_offset(self):
        url = "https://maps.googleapis.com/maps/api/timezone/json?"

        api_params = {
            'location': self.user_coord,
            'timestamp': self.utc_stamp,
            'sensor':'true'
        }

        tz_result = requests.get(url,params=api_params)
        tz_result_json = tz_result.json()

        self.tz_id = tz_result_json['timeZoneId']

        # Need to convert weather resutls epoch
        self.tz_offset = tz_result_json['dstOffset'] + tz_result_json['rawOffset']

    def set_current_dt(self):
        self.get_tz_offset()
        self.current_dt = datetime.fromtimestamp(self.utc_stamp, timezone(self.tz_id))

# Get sunrise and sunset from earthtools
class DayResolver(object):
    def __init__(self, lat, lng, date):
        self.lat = lat
        self.lng = lng
        self.date = date
        self.is_day = None

    def get_earthtools(self):
        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        earth_final_url=earth_url%(self.lat,self.lng,self.date.day,self.date.month)

        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)

    def get_is_day(self):
        sun_position = self.get_earthtools()

        sunrise = datetime.strptime(sun_position.sunrise.string, '%H:%M:%S').time()
        sunset = datetime.strptime(sun_position.sunset.string, '%H:%M:%S').time()
            
        if sunrise < self.date.time() < sunset:
            self.is_day = True
        else:
            self.is_day = False

class WeatherFetcher(object):
    def __init__(self, location, desired_date):
        self._called = False
        self.location = location
        self.desired_date = desired_date

    @property
    def weather(self):
        self._call_api()
        self._weather
    @property
    def moon(self):
        self._call_api()
        self._moon

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
