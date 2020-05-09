# Function to perfom calls to APIs then store raw JSON responses
def call_apis(location_lat, 
              location_lon):
    from requests import get
    from application import application
    import os

    opwm_cel_api = get(f"https://api.openweathermap.org/data/2.5/weather"
                       f"?lat={location_lat}&lon={location_lon}"
                       f"&appid={application.config['OPWM_API_KEY']}&units=metric").json()
    
    opwm_fah_api = get(f"https://api.openweathermap.org/data/2.5/weather"
                       f"?lat={location_lat}&lon={location_lon}"
                       f"&appid={application.config['OPWM_API_KEY']}&units=imperial").json()

    opwm_cel_forecast_api = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                f"?lat={location_lat}&lon={location_lon}"
                                f"&appid={application.config['OPWM_API_KEY']}&units=metric").json()

    opwm_fah_forecast_api = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                f"?lat={location_lat}&lon={location_lon}"
                                f"&appid={application.config['OPWM_API_KEY']}&units=imperial").json()

    opwm_uv_index_api = get(f"https://api.openweathermap.org/data/2.5/uvi"
                            f"?&appid={application.config['OPWM_API_KEY']}&lat={location_lat}"
                            f"&lon={location_lon}").json()

    timezonedb_api = get(f"http://api.timezonedb.com/v2.1/get-time-zone"
                         f"?format=json&by=position"
                         f"&lat={location_lat}&lng={location_lon}"
                         f"&key={application.config['TIMEZONEDB_API_KEY']}").json()
    
    air_quality_api = get(f"http://api.airvisual.com/v2/nearest_city"
                          f"?lat={location_lat}&lon={location_lon}"
                          f"&key={application.config['AIRQUALITY_API_KEY']}").json()
    
    # Storing raw JSON responses in a custom dictionnary to be used 
    # by the store_data_from function
    apis_responses = {
        "opwm_cel_api": opwm_cel_api,
        "opwm_fah_api": opwm_fah_api,
        "opwm_cel_forecast_api": opwm_cel_forecast_api,
        "opwm_fah_forecast_api": opwm_fah_forecast_api,
        "opwm_uv_index_api": opwm_uv_index_api,
        "timezonedb_api": timezonedb_api,
        "air_quality_api": air_quality_api
    }

    return apis_responses


# Function to alter and store values from retrieved JSON responses,
# so that they be used in corresponding templates
def store_data_from(opwm_cel_api,
                    opwm_fah_api,
                    opwm_cel_forecast_api,
                    opwm_fah_forecast_api,
                    opwm_uv_index_api,
                    timezonedb_api,
                    air_quality_api):
    from datetime import datetime
    from iso3166 import countries
    from app.weather.routes import cache
    import flag
    import portolan

    # In a dictionnary, storing raw values.
    # Some others are altered before being store
    apis_data = {}
    apis_data["country_full_name"] = (countries
                                      .get(opwm_cel_api["sys"]["country"])
                                      .name)
    apis_data["country_code"] = opwm_cel_api["sys"]["country"]
    apis_data["location_station_name"] = opwm_cel_api["name"]
    apis_data["location_more_link"] = (f"https://www.google.com/search?"
                                       f"q={cache.get('user_query_location')}")
    apis_data["location_local_time"] = (datetime
                                        .strptime(timezonedb_api["formatted"], 
                                        "%Y-%m-%d %H:%M:%S"))
    apis_data["weather_time_calc_utc_current"] = (datetime
                                                  .fromtimestamp(opwm_cel_api["dt"])
                                                  .strftime("%d/%m/%Y, at %H:%M"))
    apis_data["weather_time_calc_utc_forecast"] = ([datetime
                                                    .strptime(time_calc["dt_txt"], 
                                                    "%Y-%m-%d %H:%M:%S")
                                                    for time_calc 
                                                    in opwm_cel_forecast_api["list"]])
    apis_data["weather_description"] = (opwm_cel_api["weather"][0]["description"]
                                        .capitalize())
    apis_data["weather_pressure"] = opwm_cel_api["main"]["pressure"]
    apis_data["weather_humidity"] = opwm_cel_api["main"]["humidity"]
    apis_data["weather_air_quality_index"] = air_quality_api["data"]["current"]["pollution"]["aqius"]
    apis_data["country_emoji_flag"] = (flag
                                       .flagize(f":{opwm_cel_api['sys']['country']}:"))
    apis_data["weather_uv_index"] = round(opwm_uv_index_api["value"])
    apis_data["weather_cel_temp_current"] = round(opwm_cel_api["main"]["temp"], 1)
    apis_data["weather_cel_temp_forecast"] = [round(temp["main"]["temp"], 1) 
                                              for temp 
                                              in opwm_cel_forecast_api["list"]]
    apis_data["weather_cel_feels_like"] = round(opwm_cel_api["main"]["feels_like"], 1)
    apis_data["weather_cel_feels_like_forecast"] = [round(temp["main"]["feels_like"], 1)
                                                    for temp 
                                                    in opwm_cel_forecast_api["list"]]
    apis_data["weather_cel_temp_min"] = round(opwm_cel_api["main"]["temp_min"], 1)
    apis_data["weather_cel_temp_max"] = round(opwm_cel_api["main"]["temp_max"], 1)
    apis_data["weather_cel_wind_speed"] = round(opwm_cel_api["wind"]["speed"], 1)
    apis_data["weather_fah_temp_current"] = round(opwm_fah_api["main"]["temp"], 1)
    apis_data["weather_fah_temp_forecast"] = [round(temp["main"]["temp"], 1)
                                              for temp 
                                              in opwm_fah_forecast_api["list"]]
    apis_data["weather_fah_feels_like"] = round(opwm_fah_api["main"]["feels_like"], 1)
    apis_data["weather_fah_feels_like_forecast"] = [round(temp["main"]["feels_like"], 1)
                                                    for temp 
                                                    in opwm_fah_forecast_api["list"]]
    apis_data["weather_fah_temp_min"] = round(opwm_fah_api["main"]["temp_min"], 1)
    apis_data["weather_fah_temp_max"] = round(opwm_fah_api["main"]["temp_max"], 1)
    apis_data["weather_fah_wind_speed"] = round(opwm_fah_api["wind"]["speed"], 1)
    apis_data["table_forecast"] = {"table_weather_description" : [descr["weather"][0]["description"].capitalize()
                                                                  for descr
                                                                  in opwm_cel_forecast_api["list"][::3]],
                                    "table_weather_icon" : [ico['weather'][0]['icon']
                                                            for ico 
                                                            in opwm_cel_forecast_api["list"][::3]],
                                   "table_weather_humidity" : [level["main"]["humidity"] 
                                                               for level
                                                               in opwm_cel_forecast_api["list"][::3]],
                                   "table_weather_cel_wind_speed": [round(speed["wind"]["speed"], 1)
                                                                    for speed
                                                                    in opwm_cel_forecast_api["list"][::3]],
                                   "table_weather_fah_wind_speed": [round(speed["wind"]["speed"], 1)
                                                                    for speed
                                                                    in opwm_fah_forecast_api["list"][::3]]}      


    # Handling the situation when the JSON response
    # lacks the ["wind"]["deg"] key    
    try:
        apis_data["weather_wind_direction_abbr"] = (portolan
                                                    .point(degree=round(opwm_cel_api["wind"]["deg"]))
                                                    .capitalize())
    except KeyError:
        apis_data["weather_wind_direction_abbr"] = "No data"

    return apis_data