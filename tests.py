#!flask/bin/python
# -*- coding: utf8 -*-
from coverage import coverage
cov = coverage(branch = True, omit = ['env/*', 'tests.py'])

import os, pytz
import unittest
from app import new_world_weather as new
from app import app, db
from app.models import User, Location
from config import basedir
from datetime import datetime, date
from mock import patch

def _helper(**kwargs):
    return {
        'txt_query': kwargs.get('txt_query'),
        'user_coord': kwargs.get('user_coord'),
        'date': kwargs.get('date')
    }

class MainTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(email = 'john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_picture(self):
        is_day = True
        icon = "clear-day"
        moonphase = "Full Moon"

        picture_details = new.choose_picture(icon, moonphase, is_day)

        assert picture_details[0] == "sun"
        assert picture_details[1] == "sun_samp2.png"

    def test_datetime(self):
        local_tz = 'America/Los_Angeles'
        as_of_ts = 1382166000.0

        as_of_test = new.local_datetime(as_of_ts, local_tz)

        assert as_of_test == datetime(2013, 10, 19).date()
        # "2013-10-19"

class InputResolverTests(unittest.TestCase):

    def test_location(self):
        stored_location = 'Mission Dolores'
        fetched_location = 'mission'

# Error - model location does not exist

        # self._test_for_location(stored_location, 37.76, -122.4148, stored_location)
        self._test_for_location(fetched_location, 37.764488, -122.42685, 'Mission Dolores Gift Shop')

    def _test_for_location(self, txt_query, expected_lat, expected_lng, expected_name):

        clean_input = new.InputResolver(**_helper(txt_query=txt_query, user_coord='37.7655,-122.4429'))
        clean_input.resolve_location()

        assert clean_input.lat == expected_lat
        assert clean_input.lng == expected_lng
        assert clean_input.location_name == expected_name

    def test_date(self):
        no_date = ''
        user_date = '01-12-2011'

        # self._test_for_date(no_date, '?') - need pach to force the date
        self._test_for_date(user_date, 1294819200.0)

    def _test_for_date(self, user_date, expected):
        clean_input = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429', date=user_date))

        assert clean_input.as_of_ts == expected

class TimezoneResolverTests(unittest.TestCase):

    # time.time as of 10/17/2013 2:58 a utc
    # @patch('app.new_world_weather.time')
    def test_timezone(self):
    # def test_timezone(self, mock_time):
    #     mock_time = lambda:1382065165.548
        location_tz = new.TimezoneResolver('37.7655,-122.4429')
        assert location_tz.timezone.zone == 'America/Los_Angeles'
        assert location_tz.offset == -25200
        # How to test datetime content?

class DayResolverTests(unittest.TestCase):
    def test_conditions(self):
        noon = datetime(2013, 10, 20, 12,  tzinfo=pytz.timezone('America/Los_Angeles'))
        midnight = datetime(2013, 10, 20, 23,  tzinfo=pytz.timezone('America/Los_Angeles'))

        # Test conditions
        self._test_for_time(noon, True)
        self._test_for_time(midnight, False)

    def _test_for_time(self, time, expected):
        lat = 37.7655
        lng = -122.4429

        day_resolve = new.DayResolver(lat, lng, time)
        assert day_resolve.is_day == expected

class WeatherFetcherTests(unittest.TestCase):

    def test_conditions(self):
        local_tz = 'America/Los_Angeles'

        current_date_day = datetime(2013, 10, 19, 12,  tzinfo=pytz.timezone(local_tz))
        future_date_day = datetime(2013, 10, 20, 12,  tzinfo=pytz.timezone(local_tz))

        current_date_night = datetime(2013, 10, 19, 23,  tzinfo=pytz.timezone(local_tz))
        future_date_night = datetime(2013, 10, 20, 23,  tzinfo=pytz.timezone(local_tz))

        self._test_for_weather(current_date_day, None)
        self._test_for_weather(future_date_day, None)

#FIX - use patch to set the value
        self._test_for_moon(current_date_night, "Full Moon")
        self._test_for_moon(future_date_night, "Full Moon")

    def _test_for_weather(self, as_of, expected):
        lat = 37.7655
        lng = -122.4429        
        offset = -25200

        fetcher = new.WeatherFetcher(lat, lng, as_of, offset)

        assert fetcher.weather["icon"] != expected
        assert fetcher.weather["temp_F"] != expected
        assert fetcher.weather["temp_C"] != expected
        assert fetcher.weather["wind_gust_mph"] != expected
        assert fetcher.weather["humidty"] != expected
        assert fetcher.weather["high_F"] != expected
        assert fetcher.weather["high_C"] != expected
        assert fetcher.weather["low_F"] != expected
        assert fetcher.weather["low_C"] != expected

        # assert fetcher.weather["feelslike_f"] != expected
        # assert fetcher.weather["feelslike_c"] != expected

    def _test_for_moon(self, as_of, expected):
        lat = 37.7655
        lng = -122.4429        
        offset = -25200

        fetcher = new.WeatherFetcher(lat, lng, as_of, offset)

        assert fetcher.moon == expected

class TemplateContextTests(unittest.TestCase):
    def test_conditions(self):
        sun_details = ("sun", "sun_samp2.png")

        self._test_for_template(sun_details, "sun", "/static/img/sun_samp2.png")

    def _test_for_template(self, picture_details, expected_descrip, expected_picture):

        template = new.TemplateContext(picture_details)

        assert template.weather_description == expected_descrip
        assert template.picture_path == expected_picture

if __name__ == '__main__':
    cov.start()    
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory = 'tmp/coverage')
    cov.erase()