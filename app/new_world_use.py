
def create_template_data(txt_query, user_coord, date_submitted):
    input_confirm = new.InputResolver(txt_query, user_coord, date_submitted)
    input_cofirm.resolve_location()

    location_tz = new.TimezoneResolver(user_coord)

    is_day = new.DayResolver(input_confirm.lat, input_confirm.lng, input_confirm.as_of_ts)

    fetcher = new.WeatherFetcher(input_confirm.lat, input_confirm.lng, is_day.as_of_dt, location_tz.offset).weather

    picture = new.choose_picture(fetcher['icon'], fetcher.moon, is_day.is_day)

    return new.TemplateContext({
     'location_name': f.location_name,
     'weather_descrip': weather.description,
     })

