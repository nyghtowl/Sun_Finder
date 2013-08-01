"""
Weather_forecast 

generated object to pull weather results

"""
from config import FIO_KEY, WUI_KEY
import requests
import datetime
import time
import moonphase
from pprint import pprint

class Weather(object):
    def __init__(self, fio_response, wui_response, as_of):
        # pprint(fio_response)
        # pprint(wui_response)

        self.lat = fio_response['latitude'] # Shortest code to get to it out of results
        self.lng = fio_response['longitude']
        self.loc_name = None
        self.date = as_of
        self.print_date = as_of.strftime('%h %d, %Y') # Date for html
        # FIX change revise time based on what is submitted
        self.time = None  
        self.sun_result = None
        self.moonphase = None
        self.pic = None
        self.days = {}

        # Determine if date is current or future to determine what data points to pull
        if as_of.date() == datetime.date.today():
            self.apply_current(fio_response, wui_response)
        else:
            (fio_fragment, wui_fragment) = self.find_for(fio_response, wui_response, as_of)
            self.apply_for(fio_fragment, wui_fragment)

    # Sets up the data points for current date
    def apply_current(self, fio_response, wui_response):
        self.fio_sunrise = int(fio_response['daily']['data'][0]['sunriseTime']) # Not in wui
        self.fio_sunset = int(fio_response['daily']['data'][0]['sunsetTime']) # Not in wui
        self.wui_icon = wui_response['current_observation']['icon'] 

        self.tempr_wui_F = wui_response['current_observation']['temp_f']
        self.tempr_wui_C = wui_response['current_observation']['temp_c']
        self.tempr_fio_F = fio_response['currently']['temperature']
        self.h_tempr_wui_F = wui_response['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
        self.h_tempr_wui_C = wui_response['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
        self.l_tempr_wui_F = wui_response['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
        self.l_tempr_wui_C = wui_response['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
        self.feels_like_F = wui_response['current_observation']['feelslike_f']
        self.feels_like_C = wui_response['current_observation']['feelslike_c']
        
        self.cloud_cover = fio_response['currently']['cloudCover']
        self.wind_mph = wui_response['current_observation']['wind_gust_mph'] 
        self.humidity = wui_response['forecast']['simpleforecast']['forecastday'][0]['avehumidity']
        
        # mapped items that may or may not be used in the future
        #self.fio_icon = fio_response['hourly']['icon'] #first built off this icon and haven't mapped wui yet
        #self.tempr_wui_str = wui_response['current_observation']['temperature_string']
        #self.feels_like_str = wui_response['current_observation']['feelslike_string']
        #self.precipitation = fio_response['currently']['precipProbability'] #not in wui & disappeared from fio

    # Pull out the relevant dictionaries of data and passing to apply_for 
    def find_for(self, fio_response, wui_response, as_of):
        fio_fragment = wui_fragment = None

        for fragment in wui_response['forecast']['simpleforecast']['forecastday']:
            if datetime.datetime.fromtimestamp(float(fragment['date']['epoch'])).date() == as_of.date():
                wui_fragment = fragment
                break
        for fragment in fio_response['daily']['data']:
            if datetime.datetime.fromtimestamp(float(fragment['time'])).date() == as_of.date():
                fio_fragment = fragment
                break
        return (fio_fragment, wui_fragment)

    # Apply data attributes for future dates
    def apply_for(self, fio_fragment, wui_fragment):
        self.fio_sunrise = int(fio_fragment['sunriseTime']) # Not in wui
        self.fio_sunset = int(fio_fragment['sunsetTime']) # Not in wui
        self.wui_icon = wui_fragment['icon'] 

        self.tempr_wui_F = float(wui_fragment['high']['fahrenheit'])
        self.tempr_wui_C = float(wui_fragment['high']['celsius'])
        self.tempr_fio_F = fio_fragment['temperatureMax']
        self.feels_like_F = None
        self.feels_like_C = None

        self.cloud_cover = fio_fragment['cloudCover']
        self.wind_mph = wui_fragment['avewind']['mph'] 
        self.humidity = wui_fragment['avehumidity']

    # part of pair program 
    # def dict_index(wui_response):
        
    #     return wui_response['forecast']['simpleforecast']['forecastday']


    def grab_all_weather(self, fio_response, wui_response, as_of):
        # Hold multiple days of weather data to display

        if as_of == datetime.now().date():
            for i in range(4):
                as_of += datetime.timedelta(days=1)
                self.days[i] = find_for(self, fio_response, wui_response, as_of)


    #FIX Pull out by hour

    # Method called before or w/o initializing class to get the weather results
    @staticmethod
    def get_forecast(lat, lon, as_of):
        # Url to pass to Forecast.io
        fio_url="https://api.forecast.io/forecast/%s/%f,%f"
        # Pull API key from env with FIO_KEY
        fio_final_url=fio_url%(FIO_KEY, lat,lon)
        print fio_final_url
        fio_response = requests.get(fio_final_url).json()

        # Url to pass to WUI
        wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"
        # Pull API key from env with FIO_KEY
        wui_final_url=wui_url%(WUI_KEY, lat,lon)
        print wui_final_url
        wui_response = requests.get(wui_final_url).json()

        # Generated a dictionary of forecast data points pulling from both weather sources
        return Weather(fio_response, wui_response, as_of)
        
    # FIX - write function to give human results to wind speed - e.g. dress wearing, difficult to walk

    # Convert icon result to an image if day
    def add_day_pic(self, pic_loc):        
        # Holds weather images for reference
        weather_pics = {
            "clear-day":("sun", "sun_samp2.jpeg"),
            "clear":("sun", "sun_samp2.jpeg"),
            "rain":("rain", "rain.png"), 
            "snow":("snow", "snow.png"), 
            "sleet":("sleet", "sleet2.png"), 
            "fog":("fog", "foggy2.png"), 
            "cloudy":("cloudy", "cloudy.png"), 
            "mostlycloudy":("partly cloudy", "cloudy.png"),
            "partlycloudy":("partly cloudy", "partly_cloudy.png")
            }

        # FIX - confirm the terms for wui_icon

        # Apply image for conditions at time of request        
        if self.wui_icon in weather_pics:
            # Setup to return text for sun result
            self.sun_result = weather_pics[self.wui_icon][0]
            # Forces clear day result if the cloud cover is < 20%
            # or cloudy if cover is >80%
            if (self.wui_icon == 'mostlycloudy'):
                if self.cloud_cover < .20:
                    self.pic = pic_loc + weather_pics['clear-day'][1]
                elif self.cloud_cover < .80:
                    self.pic = pic_loc + weather_pics['partlycloudy'][1]
                else:
                    self.pic = pic_loc + weather_pics[self.wui_icon][1]
            elif (self.wui_icon == 'cloudy'):
                if self.cloud_cover < .20:
                    self.pic = pic_loc + weather_pics['clear-day'][1]
                elif self.cloud_cover < .80:
                    self.pic = pic_loc + weather_pics['partlycloudy'][1]
                else:
                    self.pic = pic_loc + weather_pics[self.wui_icon][1]
            elif (self.wui_icon == 'clear'):
                if self.cloud_cover < .20:
                    self.pic = pic_loc + weather_pics['clear-day'][1]
                elif self.cloud_cover > .80:
                    self.pic = pic_loc + weather_pics['cloudy'][1]
                else:
                    self.pic = pic_loc + weather_pics[self.wui_icon][1]
            else:
                self.pic = pic_loc + weather_pics[self.wui_icon][1]
        elif (self.wui_icon == 'wind'):
            if (self.cloud_cover < .20):
                self.pic = pic_loc + weather_pics['clear-day'][1]
            else:
                self.pic = pic_loc + weather_pics['partly-cloudy-day'][1]
        else:
            print 'Error finding photo for the time of day'            
        print self.pic

    # Convert icon result to an moon image if night
    def add_night_pic(self, pic_loc):
        night_pics = {
            "First Quarter":"moon_firstquarter.png", 
            "Full Moon":"full_moon1.jpg", 
            "Last Quarter":"moon_lastquarter.png", 
            "New Moon":"newmoon.png", 
            "Waning Crescent":"moon_waningcrescent.png",
            "Waning Gibbous":"moon_waninggibbous.png", 
            "Waxing Crescent":"moon_waxingcrescent.png", 
            "Waxing Gibbous":"moon_waxinggibbous.png"
            }

        moon = moonphase.main(self.date)
        print 'add_night, %s' % moon

        if moon in night_pics:
            self.pic = pic_loc + night_pics[moon]
            self.moonphase = moon
        else:
            print 'Error finding photo for the time of day'

    # Confirms time of day and pulls corresponding image
    def apply_pic(self):
        pic_loc = '/static/img/'        

        # Pull sunrise and sunset from weather results
        sunrise = datetime.datetime.fromtimestamp(self.fio_sunrise)
        sunset = datetime.datetime.fromtimestamp(self.fio_sunset)

        # Testing
        print 'apply_pic'
        print 1, type(self.cloud_cover)
        print 2, self.wui_icon
        print 3, moonphase.main(self.date)

        print 4, self.date
        print 5, sunrise
        print 6, sunset

        # Picture assigned based on time of day
        if sunrise < self.date < sunset:
            self.add_day_pic(pic_loc)
        else:
            print 'it\'s not daytime' #test

            self.add_night_pic(pic_loc)
            

    # FIX - define to generate neighborhood name
    def add_name(self, loc_name):
        self.loc_name = loc_name
        print self.loc_name

        
