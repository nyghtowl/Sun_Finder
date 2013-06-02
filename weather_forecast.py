"""
weather_forecast.py -  Weather class to manage weather data

"""
# use requests to pull information from api requests - alternative is urllib - this is more human
import requests
# leverage for reporting time result
import datetime
import time
import moonphase
from pprint import pprint

class Weather(object):
    def __init__(self, fio_response, wui_response, as_of):
        # testing
        # print "X" * 80
        # pprint(fio_response)
        # print "Y" * 80
        # pprint(wui_response)

        self.lat = fio_response['latitude'] #shortest code to get to it out of results
        self.lng = fio_response['longitude']
        self.loc_name = None
        self.date = as_of
        self.print_date = as_of.strftime('%h %d, %Y') # date for html
        #FIX change revise time based on what is submitted
        self.time = None  
        self.sun_result = None
        self.moonphase = None
        self.pic = None

        self.day0_icon = wui_response['forecast']['simpleforecast']['forecastday'][0]['icon']
        self.day1_icon = wui_response['forecast']['simpleforecast']['forecastday'][1]['icon']
        self.day2_icon = wui_response['forecast']['simpleforecast']['forecastday'][2]['icon']
        self.day3_icon = wui_response['forecast']['simpleforecast']['forecastday'][3]['icon']
        self.day0_htemp = wui_response['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
        self.day0_ltemp = wui_response['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
        self.day1_htemp = wui_response['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit']
        self.day1_ltemp = wui_response['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit']
        self.day2_htemp = wui_response['forecast']['simpleforecast']['forecastday'][2]['high']['fahrenheit']
        self.day2_ltemp = wui_response['forecast']['simpleforecast']['forecastday'][2]['low']['fahrenheit']
        self.day3_htemp = wui_response['forecast']['simpleforecast']['forecastday'][3]['high']['fahrenheit']
        self.day3_ltemp = wui_response['forecast']['simpleforecast']['forecastday'][3]['low']['fahrenheit']


        # determines if date is current or future to determine what data points to pull
        if as_of.date() == datetime.date.today():
            self.apply_current(fio_response, wui_response)
        else:
            (fio_fragment, wui_fragment) = self.find_for(fio_response, wui_response, as_of)
            self.apply_for(fio_fragment, wui_fragment)

    #sets up the data points for current date
    def apply_current(self, fio_response, wui_response):
        self.fio_sunrise = int(fio_response['daily']['data'][0]['sunriseTime']) #not in wui
        self.fio_sunset = int(fio_response['daily']['data'][0]['sunsetTime']) #not in wui
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
        
        # mapped items that may or may not be used in teh future
        #self.fio_icon = fio_response['hourly']['icon'] #first built off this icon and haven't mapped wui yet
        #self.tempr_wui_str = wui_response['current_observation']['temperature_string']
        #self.feels_like_str = wui_response['current_observation']['feelslike_string']
        #self.precipitation = fio_response['currently']['precipProbability'] #not in wui & disappeared from fio

    #looping through data to pull out the relevant dictionaries of data and passing to apply_for 
    def find_for(self, fio_response, wui_response, as_of):
        fio_fragment = wui_fragment = None

        for fragment in wui_response['forecast']['simpleforecast']['forecastday']:
            # import pdb;pdb.set_trace() - way to debug
            if datetime.datetime.fromtimestamp(float(fragment['date']['epoch'])).date() == as_of.date():
                wui_fragment = fragment
                break
        for fragment in fio_response['daily']['data']:
            if datetime.datetime.fromtimestamp(float(fragment['time'])).date() == as_of.date():
                fio_fragment = fragment
                break
        return (fio_fragment, wui_fragment)

    # apply data attributes for future dates
    def apply_for(self, fio_fragment, wui_fragment):
        self.fio_sunrise = int(fio_fragment['sunriseTime']) #not in wui
        self.fio_sunset = int(fio_fragment['sunsetTime']) #not in wui
        self.wui_icon = wui_fragment['icon'] 

        self.tempr_wui_F = float(wui_fragment['high']['fahrenheit'])
        self.tempr_wui_C = float(wui_fragment['high']['celsius'])
        self.tempr_fio_F = fio_fragment['temperatureMax']
        self.feels_like_F = None
        self.feels_like_C = None

        self.cloud_cover = fio_fragment['cloudCover']
        self.wind_mph = wui_fragment['avewind']['mph'] 
        self.humidity = wui_fragment['avehumidity']


    #FIX Pull out by hour

    # method that can be called before or without initializing the class
    @staticmethod
    def get_forecast(lat, lon, FIO_KEY, WUI_KEY, as_of):
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
        return Weather(fio_response, wui_response, as_of)
        
    # FIX - write function to give human results to wind speed - e.g. dress wearing, difficult to walk

    # convert icon result to an image if day
    def add_day_pic(self, pic_loc):        
        # holds weather images for reference
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

        #FIX - confirm the terms for wui_icon

        # apply image for conditions at time of request        
        if self.wui_icon in weather_pics:
            # setup to return text for sun result
            self.sun_result = weather_pics[self.wui_icon][0]
            # forces clear day result if the cloud cover is < 20%
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

    # convert icon result to an moon image if night
    def add_night_pic(self, pic_loc):
        night_pics = {
            "First Quarter":"firstquarter.png", 
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

    # confirms time of day and pulls corresponding image
    def apply_pic(self):
        pic_loc = '/static/img/'        

        # pull sunrise and sunset from weather results
        sunrise = datetime.datetime.fromtimestamp(self.fio_sunrise)
        sunset = datetime.datetime.fromtimestamp(self.fio_sunset)

        #testing
        print 'apply_pic'
        print 1, type(self.cloud_cover)
        print 2, self.wui_icon
        print 3, moonphase.main(self.date)

        print 4, self.date
        print 5, sunrise
        print 6, sunset

        # picture assigned based on time of day
        if sunrise < self.date < sunset:
            self.add_day_pic(pic_loc)
        else:
            print 'it\'s not daytime' #test

            self.add_night_pic(pic_loc)
            

    # FIX - define to generate neighborhood name
    def add_name(self, loc_name):
        self.loc_name = loc_name
        print self.loc_name

        
