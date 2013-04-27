"""
weather_forecast.py -  Weather class to manage weather data

"""
# use requests to pull information from api requests - alternative is urllib - this is more human
import requests
# leverage for reporting time result
import datetime
import time
import moonphase

class Weather(object):
    def __init__(self, fio_response, wui_response):
        self.lat = fio_response['latitude'] #shortest code to get to it out of results
        self.lng = fio_response['longitude']
        self.fio_icon = fio_response['hourly']['icon'] #first built off this icon and haven't mapped wui yet
        self.wui_icon = wui_response['current_observation']['icon'] 
        self.pic = None
        self.tempr_wui_F = wui_response['current_observation']['temp_f']
        self.tempr_wui_C = wui_response['current_observation']['temp_c']
        self.tempr_wui_str = wui_response['current_observation']['temperature_string']
        self.tempr_fio_F = fio_response['currently']['temperature']
        self.cloud_cover = fio_response['currently']['cloudCover']
        #FIX change name
        self.loc_name = None
        #FIX change revise time based on what is submitted
        self.time = datetime.datetime.now() # time.time() creates time stampe - switched to datetime
        self.fio_sunrise = int(fio_response['daily']['data'][0]['sunriseTime']) #not in wui
        self.fio_sunset = int(fio_response['daily']['data'][0]['sunsetTime']) #not in wui
        self.wind_mph = wui_response['current_observation']['wind_gust_mph'] 
        self.feels_like_str = wui_response['current_observation']['feelslike_string']
        self.feels_like_F = wui_response['current_observation']['feelslike_f']
        self.feels_like_C = wui_response['current_observation']['feelslike_c']
        self.humidity = fio_response['currently']['humidity']
        #self.precipitation = fio_response['currently']['precipProbability'] #not in wui & disappeared from fio
        self.mult_day = wui_response['forecast']['simpleforecast']['forecastday']

    #FIX Pull out by hour and by day

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
    def add_day_pic(self, pic_loc):        
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

        # apply image for conditions at time of request        
        if self.fio_icon in weather_pics:
            # forces clear day result if the cloud cover is < 20%
            if (self.fio_icon == 'partly-cloudy-day') and (self.cloud_cover < .20):
                self.pic = pic_loc + weather_pics['clear-day'] 
            elif (self.fio_icon == 'wind') and (self.cloud_cover < .20):
                self.pic = pic_loc + weather_pics['clear-day']
            elif (self.fio_icon == 'partly_cloudy') and (self.cloud_cover > .0):
                self.pic = pic_loc + weather_pics['cloudy']
            else:
                self.pic = pic_loc + weather_pics[self.fio_icon]
        else:
            print 'Error finding photo for the time of day'            
        
        #FIX - look at the amount of cloud cover and whether to set a > percentage to use full cloud
    
    # convert icon result to an image
    def add_night_pic(self, pic_loc):
        night_pics = {
            "New Moon":"newmoon.jpg", 
            "Waxing Crescent":"moon_waxingcrescent.jpg", 
            "First Quarter":"firstquarter.jpg", 
            "Waxing Gibbous":"moon_waxinggibbous.jpg", 
            "Full Moon":"full_moon1.jpg", 
            "Waning Gibbous":"moon_waninggibbous.jpg", 
            "Last Quarter":"moon_lastquarter.jpg", 
            "Waning Crescent":"moon_waningcrescent.jpg"
            }

        moon = moonphase.main(self.time)
        if moon in night_pics:
            self.pic = pic_loc + weather_pics['moon']
        else:
            print 'Error finding photo for the time of day'

    # confirms time of day and pulls corresponding image
    def validate_day(self, as_of=None):
        pic_loc = "/static/img/"        
        
        # FIX as_of and how to pull out results that are not current date
        # timestamp version
        # sunrise_ts =  self.fio_sunrise
        # sunset_ts = self.fio_sunset
        # request_ts = time.mktime(as_of.timetuple())

        # # picture assigned based on time of day
        # if sunrise_ts < self.time < sunset_ts:
        #     self.add_day_pic(pic_loc)
        # else:
        #     print "it's not daytime" #test

        #     self.add_night_pic(pic_loc)

        self.time = as_of
        sunrise = datetime.datetime.fromtimestamp(self.fio_sunrise)
        sunset = datetime.datetime.fromtimestamp(self.fio_sunset)

        
        #testing
        
        print self.fio_icon
        print self.wui_icon
        print moonphase.main(as_of)

        print self.time
        print sunrise
        print sunset

        # picture assigned based on time of day
        if sunrise < self.time < sunset:
            self.add_day_pic(pic_loc)
        else:
            print "it's not daytime" #test

            self.add_night_pic(pic_loc)
            

    # FIX - define to generate neighborhood name
    def location_name(self):
        pass

