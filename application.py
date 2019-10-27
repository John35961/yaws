from flask import Flask, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from werkzeug.contrib.cache import SimpleCache
from forms import CityForm
from iso3166 import countries
import flag
import portolan
from datetime import datetime
from requests import get
import os
import time

application = Flask(__name__)
cache = SimpleCache(default_timeout = 180)

OPWM_API_KEY = os.environ["OPWM_API_KEY"]
TIMEZONEDB_API_KEY = os.environ["TIMEZONEDB_API_KEY"]
AIRQUALITY_API_KEY = os.environ["AIRQUALITY_API_KEY"]

@application.route("/", methods = ["GET", "POST"])
def home():
    city_form = CityForm(request.form)

    if request.method == "POST":

        request_server_datetime = datetime.now()

        corrected_user_query_location = city_form.location.data.replace(" ","%20")

        nominatim_json_reponse = get(f"https://nominatim.openstreetmap.org/search/{corrected_user_query_location}?format=json")\
                                  .json()
        location_lat = nominatim_json_reponse[0]["lat"]
        location_lon = nominatim_json_reponse[0]["lon"]

        opwm_json_response = get(f"https://api.openweathermap.org/data/2.5/weather?lat={location_lat}&lon={location_lon}&appid={OPWM_API_KEY}&units=metric")\
                              .json()
        opwm_uv_index_json_response = get(f"https://api.openweathermap.org/data/2.5/uvi?&appid={OPWM_API_KEY}&lat={location_lat}&lon={location_lon}")\
                                        .json()
        opwm_forecast_json_response = get(f"https://api.openweathermap.org/data/2.5/forecast?lat={location_lat}&lon={location_lon}&appid={OPWM_API_KEY}&units=metric")\
                                       .json()

        try:
            cache.set("weather_wind_direction_deg", round(opwm_json_response["wind"]["deg"]))
            cache.set("weather_wind_direction_abbr", portolan.point(degree = cache.get("weather_wind_direction_deg")).capitalize())
        except KeyError:
            cache.set("weather_wind_direction_deg", None)
            cache.set("weather_wind_direction_abbr", "No data")

        timezonedb_json_response = get(f"http://api.timezonedb.com/v2.1/get-time-zone?format=json&by=position&lat={location_lat}&lng={location_lon}&key={TIMEZONEDB_API_KEY}")\
                                    .json()
        
        aq_json_response = get(f"http://api.airvisual.com/v2/nearest_city?lat={location_lat}&lon={location_lon}&key={AIRQUALITY_API_KEY}")\
                            .json()

        cache.set("user_query_location", city_form.location.data.split(",")[0].title())
        cache.set("country_code", opwm_json_response["sys"]["country"])
        cache.set("country_full_name", countries.get(opwm_json_response["sys"]["country"]).name)
        cache.set("country_emoji_flag", flag.flagize(f":{opwm_json_response['sys']['country']}:"))
        cache.set("location_station_name", opwm_json_response["name"])
        cache.set("location_more_link", f"https://www.google.com/search?q={cache.get('user_query_location')}")
        cache.set("location_local_time", datetime.strptime(timezonedb_json_response["formatted"],"%Y-%m-%d %H:%M:%S"))
        cache.set("weather_time_calc_utc", datetime.fromtimestamp(opwm_json_response["dt"]).strftime("%d/%m/%Y, at %H:%M"))
        cache.set("weather_temp_current", round(opwm_json_response["main"]["temp"], 1))
        cache.set("weather_temp_min", round(opwm_json_response["main"]["temp_min"], 1))
        cache.set("weather_temp_max", round(opwm_json_response["main"]["temp_max"], 1))
        cache.set("weather_description", opwm_json_response["weather"][0]["description"].capitalize())
        cache.set("weather_pressure", opwm_json_response["main"]["pressure"])
        cache.set("weather_humidity", opwm_json_response["main"]["humidity"])
        cache.set("weather_wind_speed", opwm_json_response["wind"]["speed"])
        cache.set("weather_uv_index", round(opwm_uv_index_json_response["value"]))
        cache.set("weather_air_quality_index", aq_json_response["data"]["current"]["pollution"]["aqius"])
        cache.set("weather_temp_forecast", [temp["main"]["temp"] for temp in opwm_forecast_json_response["list"][::5]])
        cache.set("weather_forecast_time_calc_utc", [datetime.strptime(time_calc["dt_txt"],"%Y-%m-%d %H:%M:%S") for time_calc in opwm_forecast_json_response["list"][::5]])

        city_form.location.data = ""

        return render_template("weather_report.html",
                                cache = cache, 
                                city_form = city_form)
    
    return render_template('home.html', 
                            cache = cache,
                            city_form = city_form)

@application.route("/about")
def about():
    city_form = CityForm(request.form)
    return render_template("about.html", city_form = city_form)


@application.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@application.errorhandler(500)
def not_found(e):
    city_form = CityForm(request.form)
    return render_template("500.html", 
                           raw_user_query_location=city_form.location.data), 500


if __name__ == "__main__":
    application.run(debug=True)
