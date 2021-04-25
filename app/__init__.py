from flask import Flask

def create_app():
    appli = Flask(__name__,
                        static_url_path="", 
                        static_folder="static")

    # Available environments are Production and Development
    ENV = "Development"

    appli.config.from_object(f"config.{ENV}Config")
    appli.config['VERSION'] = "1.6.0"

    from app.weather.routes import weather_blueprint
    from app.map.routes import map_blueprint
    from app.about.routes import about_blueprint
    from app.errors.routes import errors_blueprint

    appli.register_blueprint(weather_blueprint)
    appli.register_blueprint(map_blueprint, url_prefix="/map")
    appli.register_blueprint(about_blueprint, url_prefix="/about")
    appli.register_blueprint(errors_blueprint)

    return appli