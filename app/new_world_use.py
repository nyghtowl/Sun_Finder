import new_world_weather as new

def create_template_data(user_search_input):
    clean_input = new.InputResolver(user_search_input).get_name()

    tz = new.TimezoneResolver(f.location_name).resolve()
    is_day = new.DaytimeResolver(f.utc_time, tz)
    fetcher = new.WeatherFetcher(f.location, f.date)
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
        'date': kwargs.get('date'),
        'user_coord': kwargs.get('user_coord')
    }

if __name__ == '__main__':
    clean_input = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429'))
    clean_input.get_name()
    print clean_input
    # import pdb;pdb.set_trace()
    assert clean_input.location_name == 'Mission Dolores Gift Shop'


    location_tz = new.TimezoneResolver(clean_input.user_coord)
    location_tz.get_timezone()
    assert location_tz.tz_id == 'America/Los_Angeles'
    assert location.tz_id_dt == <DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>
