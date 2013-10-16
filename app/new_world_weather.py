from sun_functions import google_places_coord

class InputResolver(object):
    def __init__(self, query, date, user_coord):
        self.query = query
        self.date = date
        self.user_coord = user_coord

    def resolve(self):
        self.lat, self.lng, self.location = google_places_coord(self.query, self.user_coord)
        self.location_name = None
        self.utc_time = None
        self.date = None


class TimezoneResolver(object):
    def __init__(self, location):
        pass
    def resolve(self):
        pass


class DaytimeResolver(object):
    def __init__(self, utc_time, timezone):
        pass

class WeatherFetcher(object):
    def __init__(self, location, desired_date):
        self._called = False

    @property
    def weather(self):
        self._call_api()
        self._weather
    @property
    def moon(self):
        self._call_api()
        self._moon

    def _call_api():
        if self._called:
            return
        else:
            self._called = True
        # Url to pass to WUI 
        wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

        # Pull API key from env with FIO_KEY
        wui_final_url=wui_url%(WUI_KEY, lat, lng)
        print "weather underground url", wui_final_url

        wui_response = requests.get(wui_final_url).json()

        # Generated a dictionary of forecast data points pulling from both weather sources
        current = wui_response['current_observation']
        future = self._pick_future(self.desired_date)
        self._weather = {
        "icon": current['icon'],
        "feels_like_F": current['feelslike_f'],...

        }
        if future:
            self._weather.update({
                'high_F': future['high']['fahrenheit'],
                ...
            })

def choose_picture(is_day, weather, moon_phase):
    pass

class TemplateContext(object):
    pass
