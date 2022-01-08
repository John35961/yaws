from flask import Blueprint, render_template, request
from requests import get
from app.forms import CityForm

map_blueprint = Blueprint('map_blueprint',
                          __name__,
                          static_folder='static/map',
                          template_folder='templates')


@map_blueprint.route("/")
def map():
    city_form = CityForm(request.form)

    return render_template("map.html",
                           city_form=city_form)


@map_blueprint.route("/click")
def map_click():
    location_lat = request.args.get("lat")
    location_lon = request.args.get("lon")

    from application import application
    opwm_cel_json = get(f"https://api.openweathermap.org/data/2.5/weather"
                        f"?lat={location_lat}"
                        f"&lon={location_lon}"
                        f"&appid={application.config['OPWM_API_KEY']}"
                        f"&units=metric")\
                            .json()

    return opwm_cel_json
