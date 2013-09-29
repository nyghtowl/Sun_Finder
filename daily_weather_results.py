# Build Redis Model of Multiple Weather Data

from app import redis_db as weather_map
from config import WUI_KEY
from app.models import Location
from datetime import datetime
import app.sun_functions 
import app.weather_forecast
from pytz import timezone
import time

# r.set('test', 4)
# print r.get('test')

# def get_forecast(lat, lng, as_of, current_local_time):

#     # Url to pass to WUI
#     wui_url="http://api.wunderground.com/api/%s/conditions/forecast/q/%f,%f.json"

#     # Pull API key from env with FIO_KEY
#     wui_final_url=wui_url%(WUI_KEY, lat, lng)
#     print wui_final_url
#     return requests.get(wui_final_url).json()

# def apply_pic(local_tz):
#     if sunrise.time() < current_local_time < sunset.time():
#         add_day_pic(pic_loc)
#     else:
#         print 'it\'s not daytime' #test

#         self.add_night_pic(pic_loc, local_tz)


# def main():
# pull coordinates from local db
neighborhoods = Location.query.all()
lat = 37.7655
lng = -122.4429

utctimestamp = time.time()

timezone_id = app.sun_functions.search_coord_timezone(lat, lng, utctimestamp)
local_tz = timezone(timezone_id)
current_local_time = datetime.fromtimestamp(utctimestamp, local_tz)


# for nh in neighborhoods:
    # forecast = get_forecast(nh.lat, nh.lng, current_local_time,current_local_time)

forecast = app.weather_forecast.Weather.get_forecast(lat, lng, current_local_time,current_local_time)
forecast.apply_pic(local_tz)

# C_temp = ['current_observation']['temp_c']
# F_temp = ['current_observation']['temp_f']
C_temp = forecast.tempr_wui_C
F_temp = forecast.tempr_wui_F
img_url = forecast.pic

weather_id = (lat,lng)
# weather_details = { lat: lat, lng: lng, 'img_url': img_url ,'temp': F_temp }
# weather_details = { 'img_url': img_url ,'temp': F_temp }
weather_map.hset(1, 'lat', lat)
weather_map.hset(1, 'lng', lng)
weather_map.hset(1, 'img_url', img_url)
weather_map.hset(1, 'temp', F_temp)
x = float(weather_map.hget(1, 'lat'))
print weather_map.hkeys(1)
print weather_map.hvals(1)
print type(x)
# run api on each coordinate

# use icon to get url img
# to create hash temp and img_url


# add coord as a key to redis
# add hash as the value to redis