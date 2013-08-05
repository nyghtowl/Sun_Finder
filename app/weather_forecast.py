"""
Weather_forecast 

generated object to pull weather results

"""
from config import WUI_KEY
from datetime import datetime
from time import strftime
from pprint import pprint
import requests
import moonphase
from BeautifulSoup import BeautifulSoup


class Weather(object):
    def __init__(self, wui_response, lat, lng, as_of):
        # pprint(wui_response)

        self.lat = lat
        self.lng = lng
        self.loc_name = None
        # Datetime format including day and time
        self.date_time = as_of
        self.print_date = as_of.strftime('%h %d, %Y') # Date for html
        # FIX change revise time based on what is submitted
        self.time = None  
        self.sun_result = None
        self.moonphase = None
        self.pic = None
        self.days = {}

        # Determine if date is current or future to determine what data points to pull
        if as_of.date() == datetime.today().date():
            self.apply_current(wui_response)
        else:
            wui_fragment = self.find_for(wui_response, as_of)
            self.apply_for(wui_fragment)

    # Sets up the data points for current date
    def apply_current(self, wui_response):
        self.sunrise = self.get_sunrise()
        self.sunset = self.get_sunset()
        self.wui_icon = wui_response['current_observation']['icon'] 
        self.tempr_wui_F = wui_response['current_observation']['temp_f']
        self.tempr_wui_C = wui_response['current_observation']['temp_c']
        self.h_tempr_wui_F = wui_response['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
        self.h_tempr_wui_C = wui_response['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
        self.l_tempr_wui_F = wui_response['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
        self.l_tempr_wui_C = wui_response['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
        self.feels_like_F = wui_response['current_observation']['feelslike_f']
        self.feels_like_C = wui_response['current_observation']['feelslike_c']
        self.wind_mph = wui_response['current_observation']['wind_gust_mph'] 
        self.humidity = wui_response['forecast']['simpleforecast']['forecastday'][0]['avehumidity']
        
        # mapped items that may or may not be used in the future
        #self.fio_icon = fio_response['hourly']['icon'] #first built off this icon and haven't mapped wui yet
        #self.tempr_wui_str = wui_response['current_observation']['temperature_string']
        #self.feels_like_str = wui_response['current_observation']['feelslike_string']
        #self.precipitation = fio_response['currently']['precipProbability'] #not in wui & disappeared from fio

    # Pull out the relevant dictionaries of data and passing to apply_for 
    def find_for(self, wui_response, as_of):
        wui_fragment = None

        for fragment in wui_response['forecast']['simpleforecast']['forecastday']:
            if datetime.datetime.fromtimestamp(float(fragment['date']['epoch'])).date() == as_of.date():
                wui_fragment = fragment
                break
        return (wui_fragment)

    # Apply data attributes for future dates
    def apply_for(self, wui_fragment):
        self.sunrise = None
        self.sunset = None
        self.wui_icon = wui_fragment['icon'] 

        self.tempr_wui_F = float(wui_fragment['high']['fahrenheit'])
        self.tempr_wui_C = float(wui_fragment['high']['celsius'])
        self.feels_like_F = None
        self.feels_like_C = None

        self.wind_mph = wui_fragment['avewind']['mph'] 
        self.humidity = wui_fragment['avehumidity']

    # Hold multiple days of weather data to display
    def grab_all_weather(self, wui_response, as_of):
        if as_of == datetime.now().date():
            for i in range(4):
                as_of += datetime.timedelta(days=1)
                self.days[i] = find_for(self, wui_response, as_of)


    #FIX Pull out by hour

    # Method called before or w/o initializing class to get the weather results
    @staticmethod
    def get_forecast(lat, lng, as_of):
        # Url to pass to WUI
        wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"
        # Pull API key from env with FIO_KEY
        wui_final_url=wui_url%(WUI_KEY, lat, lng)
        print wui_final_url
        wui_response = requests.get(wui_final_url).json()

        # Generated a dictionary of forecast data points pulling from both weather sources
        return Weather(wui_response, lat, lng, as_of)

    def get_earthtools(self):
        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        self.date_time
        earth_final_url=earth_url%(self.lat,self.lng,self.date_time.day,self.date_time.month)
        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)
    # def get_location(self):
    #     home=ephem.Observer()
    #     home.lat=self.lat
    #     home.long=self.lng
    #     home.date=self.date_time

    #     return home        
        
    # def get_ephem(self):
    #     # Left off 30 sec adjustment and elevation
    #     return ephem.Sun()
    
    def get_sunrise(self):
        nextrise=self.get_earthtools()
        sunrise=nextrise.sunrise.string
        return datetime.strptime(sunrise, '%H:%M:%S') 
     
    def get_sunset(self):
        nextset=self.get_earthtools()
        sunset=nextset.sunset.string
        return datetime.strptime(sunset, '%H:%M:%S')

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
            self.pic = pic_loc + weather_pics[self.wui_icon][1]
        else:
            flash('Error finding photo for the time of day')
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

        moon = moonphase.main(self.date_time)
        print 'add_night, %s' % moon

        if moon in night_pics:
            self.pic = pic_loc + night_pics[moon]
            self.moonphase = moon
        else:
            print 'Error finding photo for the time of day'

    # Confirms time of day and pulls corresponding image
    def apply_pic(self):
        pic_loc = '/static/img/'        

        # Pull sunrise and sunset from weather results - use to pull timestamp
        # sunrise = datetime.datetime.fromtimestamp(self.sunrise)
        # sunset = datetime.datetime.fromtimestamp(self.sunset)

        # Testing
        print 'apply_pic'
        print 2, self.wui_icon
        print 3, moonphase.main(self.date_time)

        print 4, self.date_time.time()
        print 5, self.sunrise.time()
        print 6, self.sunset.time()
        print 7, self.sunrise.time()< self.date_time.time() < self.sunset.time()

        # Picture assigned based on time of day
        if self.sunrise.time() < self.date_time.time() < self.sunset.time():
            self.add_day_pic(pic_loc)
        else:
            print 'it\'s not daytime' #test

            self.add_night_pic(pic_loc)
            

    # FIX - define to generate neighborhood name
    def add_name(self, loc_name):
        self.loc_name = loc_name
        print self.loc_name

        
