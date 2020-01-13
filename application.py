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
cache = SimpleCache(default_timeout=180)

OPWM_API_KEY = os.environ["OPWM_API_KEY"]
TIMEZONEDB_API_KEY = os.environ["TIMEZONEDB_API_KEY"]
AIRQUALITY_API_KEY = os.environ["AIRQUALITY_API_KEY"]


@application.route("/", methods=["GET", "POST"])
def home():
    city_form = CityForm(request.form)

    if request.method == "POST":
        corrected_user_query_location = city_form.location.data.replace(" ","%20")
        nominatim_json = get(f"https://nominatim.openstreetmap.org/search/"
                             f"{corrected_user_query_location}"
                             f"?format=json").json()
        location_lat = nominatim_json[0]["lat"]
        location_lon = nominatim_json[0]["lon"]

        opwm_cel_json = get(f"https://api.openweathermap.org/data/2.5/weather"
                            f"?lat={location_lat}"
                            f"&lon={location_lon}"
                            f"&appid={OPWM_API_KEY}"
                            f"&units=metric")\
                                .json()
        
        opwm_far_json = get(f"https://api.openweathermap.org/data/2.5/weather"
                            f"?lat={location_lat}"
                            f"&lon={location_lon}"
                            f"&appid={OPWM_API_KEY}"
                            f"&units=imperial")\
                                .json()

        opwm_cel_forecast_json = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                     f"?lat={location_lat}"
                                     f"&lon={location_lon}"
                                     f"&appid={OPWM_API_KEY}"
                                     f"&units=metric")\
                                        .json()

        opwm_far_forecast_json = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                     f"?lat={location_lat}"
                                     f"&lon={location_lon}"
                                     f"&appid={OPWM_API_KEY}"
                                     f"&units=imperial")\
                                        .json()

        opwm_uv_index_json = get(f"https://api.openweathermap.org/data/2.5/uvi"
                                 f"?&appid={OPWM_API_KEY}"
                                 f"&lat={location_lat}"
                                 f"&lon={location_lon}")\
                                    .json()

        timezonedb_json = get(f"http://api.timezonedb.com/v2.1/get-time-zone"
                                       f"?format=json"
                                       f"&by=position"
                                       f"&lat={location_lat}"
                                       f"&lng={location_lon}"
                                       f"&key={TIMEZONEDB_API_KEY}")\
                                           .json()
        
        air_quality_json = get(f"http://api.airvisual.com/v2/nearest_city"
                               f"?lat={location_lat}"
                               f"&lon={location_lon}"
                               f"&key={AIRQUALITY_API_KEY}")\
                                   .json()
 
        try:
            cache.set("weather_wind_direction_deg", 
                      round(opwm_cel_json["wind"]["deg"]))
            cache.set("weather_wind_direction_abbr", 
                      portolan.point(degree=cache.get("weather_wind_direction_deg"))\
                        .capitalize())
        except KeyError:
            cache.set("weather_wind_direction_deg", 
                      None)
            cache.set("weather_wind_direction_abbr", 
                      "No data")

        cache.set("user_query_location", 
                  city_form.location.data.split(",")[0]\
                    .title())
        cache.set("country_code", 
                  opwm_cel_json["sys"]["country"])
        cache.set("country_full_name", 
                  countries.get(opwm_cel_json["sys"]["country"]).name)
        cache.set("country_emoji_flag", 
                  flag.flagize(f":{opwm_cel_json['sys']['country']}:"))
        cache.set("location_station_name", 
                  opwm_cel_json["name"])
        cache.set("location_more_link", 
                  f"https://www.google.com/search"
                  f"?q={cache.get('user_query_location')}")
        cache.set("location_local_time", 
                  datetime.strptime(timezonedb_json["formatted"],
                  "%Y-%m-%d %H:%M:%S"))
        cache.set("weather_time_calc_utc_current", 
                  datetime.fromtimestamp(opwm_cel_json["dt"])\
                    .strftime("%d/%m/%Y, at %H:%M"))
        cache.set("weather_time_calc_utc_forecast", 
                  [datetime.strptime(time_calc["dt_txt"], 
                  "%Y-%m-%d %H:%M:%S") for time_calc in opwm_cel_forecast_json["list"][::5]])
        cache.set("weather_description", 
                  opwm_cel_json["weather"][0]["description"]\
                    .capitalize())
        cache.set("weather_pressure", 
                  opwm_cel_json["main"]["pressure"])
        cache.set("weather_humidity", 
                  opwm_cel_json["main"]["humidity"])
        cache.set("weather_uv_index", 
                  round(opwm_uv_index_json["value"]))
        cache.set("weather_air_quality_index", 
                  air_quality_json["data"]["current"]["pollution"]["aqius"])

        cache.set("weather_cel_temp_current", 
                  round(opwm_cel_json["main"]["temp"], 1))
        cache.set("weather_cel_temp_min", 
                  round(opwm_cel_json["main"]["temp_min"], 1))
        cache.set("weather_cel_temp_max", 
                  round(opwm_cel_json["main"]["temp_max"], 1))
        cache.set("weather_cel_wind_speed", 
                  round(opwm_cel_json["wind"]["speed"], 1))
        cache.set("weather_cel_temp_forecast", 
                  [temp["main"]["temp"] for temp in opwm_cel_forecast_json["list"][::5]])

        cache.set("weather_far_temp_current", 
                  round(opwm_far_json["main"]["temp"], 1))
        cache.set("weather_far_temp_min", 
                  round(opwm_far_json["main"]["temp_min"], 1))
        cache.set("weather_far_temp_max", 
                  round(opwm_far_json["main"]["temp_max"], 1))
        cache.set("weather_far_wind_speed", 
                  round(opwm_far_json["wind"]["speed"], 1))
        cache.set("weather_far_temp_forecast", 
                  [temp["main"]["temp"] for temp in opwm_far_forecast_json["list"][::5]])

        city_form.location.data = ""

        return render_template("weather_report.html",
                               cache=cache, 
                               city_form=city_form)
    
    return render_template("home.html", 
                           cache=cache,
                           city_form=city_form)


@application.route("/about")
def about():
    city_form = CityForm(request.form)

    return render_template("about.html", 
                           city_form=city_form)


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
