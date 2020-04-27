from flask import Flask

application = Flask(__name__)

from weather.routes import weather_blueprint
from map.routes import map_blueprint
from about.routes import about_blueprint
from errors.routes import errors_blueprint

application.register_blueprint(weather_blueprint)
application.register_blueprint(map_blueprint, url_prefix="/map")
application.register_blueprint(about_blueprint, url_prefix="/about")
application.register_blueprint(errors_blueprint)

if __name__ == "__main__":
    application.run(debug=True)
