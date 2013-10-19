
def create_template_data(user_search_input):
    clean_input = new.InputResolver(user_search_input)
    clean_input.get_name()
    clean_input.set_date()

    is_day = new.DayResolver(clean_input.lat, clean_input.lng, clean_input.location_dt)

    fetcher = new.WeatherFetcher(clean_input.lat, clean_input.lng, clean_input.location_dt)

    weather_data = fetcher.get_weather()
    moon_phase = fetcher.moon()

    picture = new.choose_picture(is_day, weather, moon_phase)

    return new.TemplateContext({
     'location_name': f.location_name,
     'weather_descrip': weather.description,
     })

