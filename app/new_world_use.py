import new_world_weather as new

def input_to_context(parameters):
    f = new.InputForm(parameters)

    tz = new.TimezoneResolver(f.location).resolve()
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
    # input_to_context(_helper(query='mission'))
    f = new.InputResolver(**_helper(query='mission', user_coord='37.7655,-122.4429'))
    f.resolve()
    # import pdb;pdb.set_trace()
    assert f.location == 'Mission Dolores Gift Shop'