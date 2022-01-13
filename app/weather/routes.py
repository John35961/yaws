from flask import Blueprint, render_template, request
from requests import get
from werkzeug.contrib.cache import SimpleCache
from app.forms import CityForm

cache = SimpleCache()

from app.weather.functions import (call_apis,
                                   store_data_from)

weather_blueprint = Blueprint('weather_blueprint',
                              __name__,
                              static_folder='static/weather',
                              template_folder='templates')

locations_counter = []
user_recent_locations_data = []

@weather_blueprint.route("/", methods=["GET", "POST"])
def home():
    city_form = CityForm(request.form)

    # Handling POST request when CityForm is submitted
    if request.method == "POST":
        corrected_user_query_location = city_form.location.data.replace(" ","%20")
        nominatim_api = get(f"https://nominatim.openstreetmap.org/search/"
                            f"{corrected_user_query_location}?format=json").json()
        location_lat = nominatim_api[0]["lat"]
        location_lon = nominatim_api[0]["lon"]
        
        apis_responses = call_apis(location_lat, 
                                   location_lon)
        
        apis_data = store_data_from(apis_responses["opwm_cel_api"],
                                    apis_responses["opwm_fah_api"],
                                    apis_responses["opwm_cel_forecast_api"],
                                    apis_responses["opwm_fah_forecast_api"],
                                    apis_responses["opwm_uv_index_api"],
                                    apis_responses["timezonedb_api"],
                                    apis_responses["air_quality_api"])

        locations_counter.append(city_form.location.data.split(",")[0].title())
        locations_counter.reverse()

        cache.set("locations_counter", 
                  locations_counter)

        user_recent_locations_data.append(
            [city_form.location.data.split(",")[0].title(),
             apis_data["country_code"],
             apis_data["weather_cel_temp_current"],
             apis_data["weather_cel_icon_current"],
             apis_data["weather_description"]
             ])
        user_recent_locations_data.reverse()

        cache.set("user_recent_locations_data", 
                  user_recent_locations_data)
        
        city_form.location.data = ""

        return render_template("dashboard.html",
                                location_lat=location_lat,
                                location_lon=location_lon,
                                apis_data=apis_data,
                                cache=cache, 
                                city_form=city_form)

    # Handling GET request when the 'location' parameter is used in the URL
    elif request.method == "GET" and request.args.get("location"):
        corrected_user_query_location = request.args.get("location").replace(" ","%20")
        nominatim_api = get(f"https://nominatim.openstreetmap.org/search/"
                            f"{corrected_user_query_location}?format=json").json()
        location_lat = nominatim_api[0]["lat"]
        location_lon = nominatim_api[0]["lon"]
       
        apis_responses = call_apis(location_lat, 
                                   location_lon)
        
        apis_data = store_data_from(apis_responses["opwm_cel_api"],
                                    apis_responses["opwm_fah_api"],
                                    apis_responses["opwm_cel_forecast_api"],
                                    apis_responses["opwm_fah_forecast_api"],
                                    apis_responses["opwm_uv_index_api"],
                                    apis_responses["timezonedb_api"],
                                    apis_responses["air_quality_api"])
        
        locations_counter.append(request.args.get("location"))
        locations_counter.reverse()

        cache.set("locations_counter", 
                  locations_counter)

        user_recent_locations_data.append(
            [request.args.get("location"),
             apis_data["country_code"],
             apis_data["weather_cel_temp_current"],
             apis_data["weather_cel_icon_current"],
             apis_data["weather_description"]
             ])
        user_recent_locations_data.reverse()

        cache.set("user_recent_locations_data", 
                  user_recent_locations_data)

        city_form.location.data = ""

        return render_template("dashboard.html",
                                location_lat=location_lat,
                                location_lon=location_lon,
                                apis_data=apis_data,
                                cache=cache, 
                                city_form=city_form)

    # Handling GET request with no parameter
    return render_template("home.html", 
                            cache=cache,
                            city_form=city_form)


@weather_blueprint.route("/top-searches")
def top_searches():
    city_form = CityForm(request.form)

    from collections import Counter, OrderedDict
    top_searches = Counter(locations_counter)
    ordered_top_searches = OrderedDict(top_searches.most_common())

    return render_template("top-searches.html",
                            city_form=city_form,
                            ordered_top_searches=ordered_top_searches)