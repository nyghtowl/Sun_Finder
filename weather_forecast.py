"""
weather_forecast.py -  Weather class to manage weather data

"""
# use requests to pull information from api requests - alternative is urllib - this is more human
import requests
# leverage for reporting time result
import datetime
import time

class Weather(object):
    def __init__(self, fio_response, wui_response):
        self.lat = None
        self.lng = None
        self.fio_icon = fio_response['hourly']['icon']
        self.wui_icon = None
        self.pic = None
        self.tempr_wui_F = wui_response['current_observation']['temp_f']
        self.tempr_wui_C = wui_response['current_observation']['temp_c']
        self.tempr_wui_str = wui_response['current_observation']['temperature_string']
        self.tempr_fio_F = fio_response['currently']['temperature']
        self.cloud_cover = fio_response['currently']['cloudCover']
        #FIX change name
        self.loc_name = ''
        #FIX change how time is listed
        self.time = time.time()
        self.fio_sunrise = int(fio_response['daily']['data'][0]['sunriseTime'])
        self.fio_sunset = int(fio_response['daily']['data'][0]['sunsetTime'])
        self.wind_gust_mph = wui_response['current_observation']['wind_gust_mph']
        self.feels_like_str = wui_response['current_observation']['feelslike_string']
        self.feels_like_F = wui_response['current_observation']['feelslike_f']
        self.feels_like_C = wui_response['current_observation']['feelslike_c']
        self.mult_day = wui_response['forecast']['simpleforecast']['forecastday']
        
    # method that can be called before or without initializing the class
    @staticmethod
    def get_forecast(lat, lon, FIO_KEY, WUI_KEY):
        # url to pass to Forecast.io
        fio_url="https://api.forecast.io/forecast/%s/%f,%f"
        # pull API key from env with FIO_KEY
        fio_final_url=fio_url%(FIO_KEY, lat,lon)
        print fio_final_url
        fio_response = requests.get(fio_final_url).json()

        # url to pass to WUI
        wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"
        # pull API key from env with FIO_KEY
        wui_final_url=wui_url%(WUI_KEY, lat,lon)
        print wui_final_url
        wui_response = requests.get(wui_final_url).json()

        # generated a dictionary of forecast data points pulling from both weather sources
        return Weather(fio_response, wui_response)
        
    # FIX - write function to give human results to wind speed - e.g. dress wearing, difficult to walk

    # convert icon result to an image
    def add_pic(self):
        pic_location = "/static/img/"
        
        # holds weather images for reference
        weather_pics = {
            "clear-day":"sun_samp2.jpeg", 
            "rain":"rain.png" , 
            "snow":"snow.png", 
            "sleet":"sleet2.png", 
            "fog":"foggy2.png" , 
            "cloudy":"cloudy.png", 
            "partly-cloudy-day":"partly_cloudy.png"
        }
        
        # FIX how to handle wind icon result and night 

        if self.fio_icon in weather_pics:
            # forces clear day result if the cloud cover is < 20%
            if (self.fio_icon == 'partly-cloudy-day') & (self.cloud_cover < .20):
                self.pic = pic_location + weather_pics['clear-day'] 
            else:
                #print weather_pics[icon]
                self.pic = pic_location + weather_pics[icon]

        #FIX - what happends if not result
                
    # pulls forecast information from work on incorporating as_of
    def validate_day(self, as_of=None):
        
        # FIX as_of and how to pull out results that are not current date

        print self.fio_icon
        print as_of

        # sunrise_ts = datetime.datetime.utcfromtimestamp(self.fio_sunrise)
        # sunset_ts = datetime.datetime.utcfromtimestamp(self.fio_sunset)
        sunrise_ts =  self.fio_sunrise
        sunset_ts = self.fio_sunset
        print sunrise_ts
        print sunset_ts

        # condition to only show sun in the daytime based on sunrise and sunset
        if sunrise_ts < self.time < sunset_ts:
            self.add_pic()
        else:

            # FIX print a result if not daytime in that timezone
            
            print "it's not daytime"

    # FIX - rework this format...
    # def day_format(self):

    #   fio_rise = fio_response['daily']['data'][0]['sunriseTime']
    #   fio_set = fio_response['daily']['data'][0]['sunsetTime']

    #   sunrise = datetime.datetime.utcfromtimestamp(fio_rise)
    #   sunset = datetime.datetime.utcfromtimestamp(fio_set)
