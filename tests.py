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
from datetime import datetime, timedelta, date, time
from mock import patch
# import moonphase

# mock api results

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
        self.assertEqual(avatar[0:len(expected)], expected)

    def test_picture(self):
        is_day = True
        icon = "clear-day"
        moonphase = "Full Moon"

        picture_details = new.choose_picture(icon, moonphase, is_day)

        self.assertEqual(picture_details[0], "sun")
        self.assertEqual(picture_details[1], "sun_samp2.png")

class InputResolverTests(unittest.TestCase):
    def setUp(self):
        self.user_coord = '37.7655,-122.4429'

    def tearDown(self):
        pass

    def test_location(self):
        stored_location = 'Mission District'
        fetched_location = 'mission'

        self._test_for_location(stored_location, 37.76, -122.4148, u'Mission District')
        self._test_for_location(fetched_location, 37.764488, -122.42685, 'Mission Dolores Gift Shop')

    def _test_for_location(self, txt_query, expected_lat, expected_lng, expected_name):

        clean_input = new.InputResolver(**_helper(txt_query=txt_query, user_coord=self.user_coord))

        self.assertEqual(clean_input.lat, expected_lat)
        self.assertEqual(clean_input.lng, expected_lng)
        self.assertEqual(clean_input.location_name, expected_name)

    def test_date(self):
        no_date = ''
        user_date = '01-12-2011'
        user_date_ts = 1294878180.0

        # FIX - need to patch a value that doesn't change with time
        self._test_for_date(no_date)
        self._test_for_date(user_date)

    def _test_for_date(self, user_date):
        clean_input = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429', date=user_date))

        self.assertIsNotNone(clean_input.as_of_ts)

class TimezoneResolverTests(unittest.TestCase):
    # time.time as of 10/17/2013 2:58 a utc
    # @patch('app.new_world_weather.time')
    def test_timezone(self):
    # def test_timezone(self, mock_time):
    #     mock_time = lambda:1382065165.548
        location_tz = new.TimezoneResolver('37.7655,-122.4429')

        self.assertEqual(location_tz.timezone.zone,'America/Los_Angeles')
        self.assertEqual(location_tz.offset, -25200)

class DayResolverTests(unittest.TestCase):
    def setUp(self):
        self.lat = 37.7655
        self.lng = -122.4429
        self.offset = -25200

    def tearDown(self):
        pass

    def test_conditions(self):
        noon = 1382295600.0
        midnight = 1382335200.0

        self._test_for_time(noon, True, datetime(2013, 10, 20, 12, 0), self.offset)
        self._test_for_time(midnight, False, datetime(2013, 10, 20, 23, 0), self.offset)

    def _test_for_time(self, as_of_ts, expected_is_day, expected_as_of, offset):
        day_resolve = new.DayResolver(self.lat, self.lng, as_of_ts, offset)
        self.assertEqual(day_resolve.is_day, expected_is_day)
        self.assertEqual(day_resolve.as_of_dt, expected_as_of)
# FIX - Potentially not work when posted on server - need to account for what time is being set?

class WeatherFetcherTests(unittest.TestCase):
    def setUp(self):
        local_tz = 'America/Los_Angeles'
        current_date = datetime.utcnow().replace(tzinfo = pytz.timezone(local_tz)).date()
        future_date = current_date + timedelta(days=2)
        day = time(12, 0)
        night = time(23, 0)

        self.current_day = datetime.combine(current_date, day)
        self.current_night = datetime.combine(current_date, night)
        self.future_day = datetime.combine(current_date, day)
        self.future_night = datetime.combine(future_date, night)

        self.lat = 37.7655
        self.lng = -122.4429        
        self.offset = -25200

    def tearDown(self):
        pass

    def test_conditions(self):

        self._test_for_weather(self.current_day)
        self._test_for_weather(self.current_night)

        self._test_current_conditions(self.current_day)
        self._test_current_conditions(self.current_night)

        self._test_for_weather(self.future_day)
        self._test_for_weather(self.future_night)

    def _test_for_weather(self, as_of):

        fetcher = new.WeatherFetcher(self.lat, self.lng, as_of, self.offset)

        self.assertIsNotNone(fetcher.weather["icon"])
        self.assertIsNotNone(fetcher.weather["temp_F"])
        self.assertIsNotNone(fetcher.weather["temp_C"])
        self.assertIsNotNone(fetcher.weather["wind_gust_mph"])
        self.assertIsNotNone(fetcher.weather["humidty"])
        self.assertIsNotNone(fetcher.weather["high_F"])
        self.assertIsNotNone(fetcher.weather["high_C"])
        self.assertIsNotNone(fetcher.weather["low_F"])
        self.assertIsNotNone(fetcher.weather["low_C"])

        self.assertIsNotNone(fetcher.moon)

    def _test_current_conditions(self, as_of): 
        fetcher = new.WeatherFetcher(self.lat, self.lng, as_of, self.offset)

        self.assertIsNotNone(fetcher.weather["feels_like_F"])
        self.assertIsNotNone(fetcher.weather["feels_like_C"])

# class TemplateContextTests(unittest.TestCase):
#     def test_conditions(self):
#         sun_details = ("sun", "sun_samp2.png")

#         self._test_for_template(sun_details, "sun", "/static/img/sun_samp2.png")

#     def _test_for_template(self, picture_details, expected_descrip, expected_picture):

#         template = new.TemplateContext(picture_details)

#         assert template.weather_description == expected_descrip
#         assert template.picture_path == expected_picture

if __name__ == '__main__':
    cov.start()    
    try:
        unittest.main(verbosity=2)
    except:
        pass
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory = 'tmp/coverage')
    cov.erase()