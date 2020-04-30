from flask import Blueprint, render_template, request
from app.forms import CityForm

about_blueprint = Blueprint('about_blueprint',
                            __name__,
                            template_folder='templates')

@about_blueprint.route("/")
def about():
    city_form = CityForm(request.form)
    return render_template("about.html",
                           city_form=city_form)