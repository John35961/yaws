from flask import Blueprint, render_template, request
from app.forms import CityForm

errors_blueprint = Blueprint('errors_blueprint',
                            __name__,
                            template_folder='templates')

@errors_blueprint.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@errors_blueprint.app_errorhandler(500)
def not_found(e):
    city_form = CityForm(request.form)
    
    return render_template("500.html", 
                           raw_user_query_location=city_form.location.data), 500