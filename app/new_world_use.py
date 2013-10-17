import new_world_weather as new

# For tests
from datetime import datetime

def create_template_data(user_search_input):
    clean_input = new.InputResolver(user_search_input)
    clean_input.get_name()
    clean_input.set_date()

    is_day = new.DayResolver(clean_input.lat, clean_input.lng, clean_input.location_dt)

    fetcher = new.WeatherFetcher(clean_input.location_name, clean_input.location_dt)

    weather = fetcher.weather()
    moon_phase = fetcher.moon()

    picture = new.choose_picture(is_day, weather, moon_phase)

    return new.TemplateContext({
     'location_name': f.location_name,
     'weather_descrip': weather.description,
     })

def _helper(**kwargs):
    return {
        'query': kwargs.get('query'),
        'user_coord': kwargs.get('user_coord'),
        'date': kwargs.get('date')
    }

if __name__ == '__main__':
    # Test with user date inputted
    clean_input = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429', date='10-17-2013'))
    clean_input.set_date()
    assert clean_input.location_dt != None
    assert clean_input.location_dt_str == '2013-10-17'

    # Test with no inputted date
    clean_input = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429'))
    clean_input.get_name()
    clean_input.set_date()
    # import pdb;pdb.set_trace()
    assert clean_input.location_name == 'Mission Dolores Gift Shop'
    assert clean_input.location_dt != None

    location_tz = new.TimezoneResolver(clean_input.user_coord)
    location_tz.get_tz_offset()
    assert location_tz.tz_id == 'America/Los_Angeles'
    assert location_tz.tz_offset == -25200

    # assert type(location_tz.current_dt) == datetime.datetime
    # datetime.datetime(2013, 10, 16, 17, 46, 16, 598585, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>)

    day_resolve = new.DayResolver(clean_input.lat, clean_input.lng, clean_input.location_dt)
    day_resolve.get_is_day()
    assert day_resolve.is_day == True
