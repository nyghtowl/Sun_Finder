from sun_functions import google_places_coord
from pytz import timezone
import time, requests, json

class InputResolver(object):
    def __init__(self, query, date, user_coord):
        self.query = query
        self.date = date
        self.user_coord = user_coord

    # FIX - only run if not in postgres
    def get_name(self):
        # FIX - remove lat and lng?
        self.lat, self.lng, self.location_name = google_places_coord(self.query, self.user_coord)

        self.date = None

    def __str__(self):
        return ("query= " + self.query + " user_coord= " + self.user_coord + "  name= " + self.location_name)

class TimezoneResolver(object):
    def __init__(self, user_coord):
        self.tz_id = None
        self.utc_stamp = time.time()
        self.user_coord = user_coord

    def get_timezone(self):
        url = "https://maps.googleapis.com/maps/api/timezone/json?"

        api_params = {
            'location': self.user_coord,
            'timestamp': self.utc_stamp,
            'sensor':'true'
        }

        tz_result = requests.get(url,params=api_params)
        tz_result_json = tz_result.json()

        self.tz_id = tz_result_json['timeZoneId']


class DaytimeResolver(object):
    def __init__(self, utc_time, timezone):
        self.utc_time = utc_time
        self.timezone = timezone


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
