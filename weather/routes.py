from flask import Blueprint, render_template, request
from requests import get
from datetime import datetime
from iso3166 import countries
from werkzeug.contrib.cache import SimpleCache
from forms import CityForm
import flag
import portolan
import os

OPWM_API_KEY = os.environ["OPWM_API_KEY"]
TIMEZONEDB_API_KEY = os.environ["TIMEZONEDB_API_KEY"]
AIRQUALITY_API_KEY = os.environ["AIRQUALITY_API_KEY"]

weather_blueprint = Blueprint('weather_blueprint',
                              __name__,
                              static_folder='static/weather',
                              template_folder='templates')

cache = SimpleCache(default_timeout=180)


# Function to perfom calls to APIs
# then store bare JSON object responses in a custom dictionnary
def call_apis(location_lat, 
              location_lon,
              OPWM_API_KEY=OPWM_API_KEY, 
              TIMEZONEDB_API_KEY=TIMEZONEDB_API_KEY, 
              AIRQUALITY_API_KEY=AIRQUALITY_API_KEY):
    opwm_cel_api = get(f"https://api.openweathermap.org/data/2.5/weather"
                        f"?lat={location_lat}"
                        f"&lon={location_lon}"
                        f"&appid={OPWM_API_KEY}"
                        f"&units=metric")\
                            .json()
    
    opwm_far_api = get(f"https://api.openweathermap.org/data/2.5/weather"
                        f"?lat={location_lat}"
                        f"&lon={location_lon}"
                        f"&appid={OPWM_API_KEY}"
                        f"&units=imperial")\
                            .json()

    opwm_cel_forecast_api = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                    f"?lat={location_lat}"
                                    f"&lon={location_lon}"
                                    f"&appid={OPWM_API_KEY}"
                                    f"&units=metric")\
                                        .json()

    opwm_far_forecast_api = get(f"https://api.openweathermap.org/data/2.5/forecast"
                                    f"?lat={location_lat}"
                                    f"&lon={location_lon}"
                                    f"&appid={OPWM_API_KEY}"
                                    f"&units=imperial")\
                                        .json()

    opwm_uv_index_api = get(f"https://api.openweathermap.org/data/2.5/uvi"
                                f"?&appid={OPWM_API_KEY}"
                                f"&lat={location_lat}"
                                f"&lon={location_lon}")\
                                    .json()

    timezonedb_api = get(f"http://api.timezonedb.com/v2.1/get-time-zone"
                                    f"?format=json"
                                    f"&by=position"
                                    f"&lat={location_lat}"
                                    f"&lng={location_lon}"
                                    f"&key={TIMEZONEDB_API_KEY}")\
                                        .json()
    
    air_quality_api = get(f"http://api.airvisual.com/v2/nearest_city"
                            f"?lat={location_lat}"
                            f"&lon={location_lon}"
                            f"&key={AIRQUALITY_API_KEY}")\
                                .json()
    
    apis_responses = {
        "opwm_cel_api": opwm_cel_api,
        "opwm_far_api": opwm_far_api,
        "opwm_cel_forecast_api": opwm_cel_forecast_api,
        "opwm_far_forecast_api": opwm_far_forecast_api,
        "opwm_uv_index_api": opwm_uv_index_api,
        "timezonedb_api": timezonedb_api,
        "air_quality_api": air_quality_api
    }

    return apis_responses


# Function to parse retrieved JSON object responses
# then store them in a custom dictionnary
def store_data_from(opwm_cel_api,
                    opwm_far_api,
                    opwm_cel_forecast_api,
                    opwm_far_forecast_api,
                    opwm_uv_index_api,
                    timezonedb_api,
                    air_quality_api):
    apis_data = {}
    apis_data["country_code"] = opwm_cel_api["sys"]["country"]
    apis_data["country_full_name"] = countries.get(opwm_cel_api["sys"]["country"]).name
    apis_data["country_emoji_flag"] = flag.flagize(f":{opwm_cel_api['sys']['country']}:")
    apis_data["location_station_name"] = opwm_cel_api["name"]
    apis_data["location_more_link"] =  f"https://www.google.com/search?q={cache.get('user_query_location')}"
    apis_data["location_local_time"] = datetime.strptime(timezonedb_api["formatted"], "%Y-%m-%d %H:%M:%S")
    apis_data["weather_time_calc_utc_current"] = datetime.fromtimestamp(opwm_cel_api["dt"]).strftime("%d/%m/%Y, at %H:%M")
    apis_data["weather_time_calc_utc_forecast"] = [datetime.strptime(time_calc["dt_txt"], "%Y-%m-%d %H:%M:%S") for time_calc in opwm_cel_forecast_api["list"][::5]]
    apis_data["weather_description"] =  opwm_cel_api["weather"][0]["description"].capitalize()
    apis_data["weather_pressure"] = opwm_cel_api["main"]["pressure"]
    apis_data["weather_humidity"] = opwm_cel_api["main"]["humidity"]
    apis_data["weather_uv_index"] = round(opwm_uv_index_api["value"])
    apis_data["weather_air_quality_index"] = air_quality_api["data"]["current"]["pollution"]["aqius"]
    apis_data["weather_cel_temp_current"] = round(opwm_cel_api["main"]["temp"], 1)
    apis_data["weather_cel_temp_min"] = round(opwm_cel_api["main"]["temp_min"], 1)
    apis_data["weather_cel_temp_max"] =  round(opwm_cel_api["main"]["temp_max"], 1)
    apis_data["weather_cel_wind_speed"] = round(opwm_cel_api["wind"]["speed"], 1)
    apis_data["weather_cel_temp_forecast"] = [temp["main"]["temp"] for temp in opwm_cel_forecast_api["list"][::5]]
    apis_data["weather_far_temp_current"] = round(opwm_far_api["main"]["temp"], 1)
    apis_data["weather_far_temp_min"] = round(opwm_far_api["main"]["temp_min"], 1)
    apis_data["weather_far_temp_max"] = round(opwm_far_api["main"]["temp_max"], 1)
    apis_data["weather_far_wind_speed"] = round(opwm_far_api["wind"]["speed"], 1)
    apis_data["weather_far_temp_forecast"] = [temp["main"]["temp"] for temp in opwm_far_forecast_api["list"][::5]]

    try:
        apis_data["weather_wind_direction_deg"] = round(opwm_cel_api["wind"]["deg"])
        apis_data["weather_wind_direction_abbr"] = portolan.point(degree=apis_data["weather_wind_direction_deg"])\
                                                            .capitalize()
    except KeyError:
        apis_data["weather_wind_direction_deg"] = None
        apis_data["weather_wind_direction_abbr"] = "No data"

    return apis_data
        

@weather_blueprint.route("/", methods=["GET", "POST"])
def home():
    city_form = CityForm(request.form)
    
    # Handling POST request when CityForm is submitted
    if request.method == "POST":
        corrected_user_query_location = city_form.location.data.replace(" ","%20")
        nominatim_api = get(f"https://nominatim.openstreetmap.org/search/"
                             f"{corrected_user_query_location}"
                             f"?format=json").json()
        location_lat = nominatim_api[0]["lat"]
        location_lon = nominatim_api[0]["lon"]

        cache.set("user_query_location", 
                  city_form.location.data.split(",")[0]\
                    .title())
        
        apis_responses = call_apis(location_lat, 
                                   location_lon)
        
        apis_data = store_data_from(apis_responses["opwm_cel_api"],
                                    apis_responses["opwm_far_api"],
                                    apis_responses["opwm_cel_forecast_api"],
                                    apis_responses["opwm_far_forecast_api"],
                                    apis_responses["opwm_uv_index_api"],
                                    apis_responses["timezonedb_api"],
                                    apis_responses["air_quality_api"])

        city_form.location.data = ""

        return render_template("dashboard.html",
                                apis_data=apis_data,
                                cache=cache, 
                                city_form=city_form)

    # Handling GET request when the 'location' parameter is used in the URL
    elif request.method == "GET" and request.args.get("location"):
        corrected_user_query_location = request.args.get("location").replace(" ","%20")
        nominatim_api = get(f"https://nominatim.openstreetmap.org/search/"
                            f"{corrected_user_query_location}"
                            f"?format=json").json()
        location_lat = nominatim_api[0]["lat"]
        location_lon = nominatim_api[0]["lon"]

        cache.set("user_query_location", 
                  request.args.get("location"))
       
        apis_responses = call_apis(location_lat, 
                                   location_lon)
        
        apis_data = store_data_from(apis_responses["opwm_cel_api"],
                                    apis_responses["opwm_far_api"],
                                    apis_responses["opwm_cel_forecast_api"],
                                    apis_responses["opwm_far_forecast_api"],
                                    apis_responses["opwm_uv_index_api"],
                                    apis_responses["timezonedb_api"],
                                    apis_responses["air_quality_api"])

        city_form.location.data = ""

        return render_template("dashboard.html",
                                apis_data=apis_data,
                                cache=cache, 
                                city_form=city_form)

    # Handling GET request with no parameter
    return render_template("home.html", 
                           city_form=city_form)