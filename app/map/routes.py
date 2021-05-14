from flask import Blueprint, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from requests import get
from app.forms import CityForm


map_blueprint = Blueprint('map_blueprint',
                          __name__,
                          static_folder='static/map',
                          template_folder='templates')

from build import initialize

limiter = Limiter(initialize,
                   key_func=get_remote_address)


@map_blueprint.route("/")
def map():
    city_form = CityForm(request.form)

    return render_template("map.html",
                           city_form=city_form)


@map_blueprint.route("/click")
@limiter.limit("60/minute")
def map_click():
    location_lat = request.args.get("lat")
    location_lon = request.args.get("lon")
    opwm_cel_json = get(f"https://api.openweathermap.org/data/2.5/weather"
                        f"?lat={location_lat}"
                        f"&lon={location_lon}"
                        f"&appid={initialize.config['OPWM_API_KEY']}"
                        f"&units=metric")\
                            .json()

    return opwm_cel_json
