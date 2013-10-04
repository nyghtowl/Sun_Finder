# Build Redis Model of Multiple Weather Data
# -*- coding: utf-8 -*-

from app import redis_db
from config import WUI_KEY
from app.models import Location
from datetime import datetime
import app.sun_functions 
import app.weather_forecast
import json
from pytz import timezone
import time


def seed_daily_weather():

    lat = 37.7655
    lng = -122.4429
    exp_time = 36000
    utctimestamp = time.time()

    timezone_id, dstOffset, rawOffset = app.sun_functions.search_coord_timezone(lat, lng, utctimestamp)
    local_tz = timezone(timezone_id)
    current_local_time = datetime.fromtimestamp(utctimestamp, local_tz)

    # pull coordinates from local db
    neighborhoods = Location.query.limit(10)

    # run api on each coordinate
    for nh in neighborhoods:

        forecast = app.weather_forecast.Weather.get_forecast(nh.lat, nh.lng, current_local_time,current_local_time, dstOffset, rawOffset)
        forecast.apply_pic(local_tz)

        range_temp = forecast.high_F + u'\xb0F' +'-' + forecast.low_F + u'\xb0F'
        img_url = forecast.pic

        weather_id = (nh.lat, nh.lng)
        weather_details = { 'lat': nh.lat, 'lng': nh.lng, 'img_url': img_url ,'temp_range':range_temp }

        print nh.lat, nh.lng

        # store coord id and hash of weather details
        redis_db.set(weather_id, json.dumps(weather_details), exp_time)

        print redis_db.get(weather_id)

if __name__ == '__main__':
    seed_daily_weather()