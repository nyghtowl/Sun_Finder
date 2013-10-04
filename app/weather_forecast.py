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
import dateutil.parser

class Weather(object):
    def __init__(self, wui_response, lat, lng, as_of, current_local_time, dstOffset, rawOffset):
        # pprint(wui_response)

        self.lat = lat
        self.lng = lng
        self.loc_name = None
        # Datetime format including day and time
        self.date_time = as_of
        self.print_date = as_of.strftime('%h %d, %Y') # Date for html
        # FIX change revise time based on what is submitted
        self.time = None  
        self.weather_descrip = None
        self.sunrise = self.get_sunrise()
        self.sunset = self.get_sunset()
        self.moonphase = None
        self.pic = None
        self.days = {}


        # Determine current or future date to figure what data to use
        forecast_frag = self.set_fragment(wui_response, as_of, dstOffset, rawOffset)
        current_frag = wui_response['current_observation']

        print "compare dates in Weather object", as_of.date(), current_local_time.date()

        if as_of.date() == current_local_time.date():
            self.apply_current(current_frag, forecast_frag)
        else:
            self.apply_forecast(forecast_frag)


    # Method called before or w/o initializing class to get the weather results
    @staticmethod
    def get_forecast(lat, lng, as_of, current_local_time, dstOffset, rawOffset):

        # Url to pass to WUI 
        wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

        # Pull API key from env with FIO_KEY
        wui_final_url=wui_url%(WUI_KEY, lat, lng)
        print "weather underground url", wui_final_url

        wui_response = requests.get(wui_final_url).json()

        # Generated a dictionary of forecast data points pulling from both weather sources
        return Weather(wui_response, lat, lng, as_of, current_local_time, dstOffset, rawOffset)
        
    # Identify api results dict/arry path based on date and set main segment to var
    def set_fragment(self, wui_response, as_of, dstOffset, rawOffset):
        wui_fragment = None

        for fragment in wui_response['forecast']['simpleforecast']['forecastday']:
            local_timestamp = float(fragment['date']['epoch']) + dstOffset +rawOffset

            # Needed timestamp offset to keep conversion of timestamp focused on search location vs location of the server
            wui_date = datetime.fromtimestamp(local_timestamp).date() 

            print "set_fragment", wui_date, as_of.date()

            if wui_date == as_of.date():
                wui_fragment = fragment
                break

        return (wui_fragment)

    # Sets up the data points for current date
    def apply_current(self, current_frag, forecast_frag):

        self.icon = current_frag['icon'] 
        self.temp_F = current_frag['temp_f']
        self.temp_C = current_frag['temp_c']
        self.feels_like_F = current_frag['feelslike_f']
        self.feels_like_C = current_frag['feelslike_c']
        self.wind_mph = current_frag['wind_gust_mph'] 

        self.high_F = forecast_frag['high']['fahrenheit']
        self.high_C = forecast_frag['high']['celsius']
        self.low_F = forecast_frag['low']['fahrenheit']
        self.low_C = forecast_frag['low']['fahrenheit']
        self.humidity = forecast_frag['avehumidity']

    # Apply data attributes for future dates
    def apply_forecast(self, wui_fragment):
        self.icon = wui_fragment['icon'] 
# looping through list to find day and then icon in dictionary

        self.temp_F = float(wui_fragment['high']['fahrenheit'])
        self.temp_C = float(wui_fragment['high']['celsius'])
        self.feels_like_F = None
        self.feels_like_C = None
        self.wind_mph = wui_fragment['avewind']['mph'] 
        self.humidity = wui_fragment['avehumidity']

    # Hold multiple days of weather data to display
    def grab_all_weather(self, wui_response, as_of):
        if as_of == datetime.now().date():
            for i in range(3):
                as_of += datetime.timedelta(days=1)
                self.days[i] = find_for(self, wui_response, as_of)


    #FIX Pull out by hour


    # Get sunrise and sunset from earthtools
    def get_earthtools(self):
        earth_url="http://www.earthtools.org/sun/%f/%f/%d/%d/99/0"
        earth_final_url=earth_url%(self.lat,self.lng,self.date_time.day,self.date_time.month)
        response_xml = requests.get(earth_final_url)
        return BeautifulSoup(response_xml.content)

    
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
            "clear-day":("sun", "sun_samp2.png"),
            "clear":("sun", "sun_samp2.png"),
            "rain":("rain", "rain.png"), 
            "snow":("snow", "snow.png"), 
            "sleet":("sleet", "sleet2.png"), 
            "fog":("fog", "foggy2.png"), 
            "cloudy":("cloudy", "cloudy.png"), 
            "mostlycloudy":("partly cloudy", "cloudy.png"),
            "partlycloudy":("partly cloudy", "partly_cloudy.png")
            }

        # Apply image for conditions at time of request        
        if self.icon in weather_pics:
            # Setup to return text for sun result
            self.weather_descrip = weather_pics[self.icon][0]
            self.pic = pic_loc + weather_pics[self.icon][1]
        else:
            flash('No photo found to match conditions.', category="info")
        print 'image url' + self.pic

    # Convert icon result to an moon image if night
    def add_night_pic(self, pic_loc, local_tz):
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

        # Pull tz to avoid error comparing tz value dt to one without
        naive_dt = self.date_time
        moon = moonphase.main(naive_dt, local_tz)
        print 'add_night, %s' % moon

        if moon in night_pics:
            self.pic = pic_loc + night_pics[moon]
            if moon.endswith("Moon"):
                self.moonphase = moon
            else:
                self.moonphase = moon + ' Moon'
        else:
            print 'Error finding photo for the time of day'

    # Confirms time of day and pulls corresponding image
    def apply_pic(self, local_tz):
        pic_loc = '/static/img/'        

        # Testing
        print "icon for pic", self.icon

        # Picture assigned based on time of day
        if self.sunrise.time() < self.date_time.time() < self.sunset.time():
            self.add_day_pic(pic_loc)
        else:
            print 'it\'s not daytime' #test

            self.add_night_pic(pic_loc, local_tz)
            

    # FIX - define to generate neighborhood name
    def add_name(self, loc_name):
        self.loc_name = loc_name
        print self.loc_name

        
