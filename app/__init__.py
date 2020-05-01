from flask import Flask

def create_app():
    application = Flask(__name__,
                        static_url_path="", 
                        static_folder="static")

    # Available environments are Production and Development
    ENV = "Production"

    application.config.from_object(f"config.{ENV}Config")
    application.config['VERSION'] = "1.5.3"

    from app.weather.routes import weather_blueprint
    from app.map.routes import map_blueprint
    from app.about.routes import about_blueprint
    from app.errors.routes import errors_blueprint

    application.register_blueprint(weather_blueprint)
    application.register_blueprint(map_blueprint, url_prefix="/map")
    application.register_blueprint(about_blueprint, url_prefix="/about")
    application.register_blueprint(errors_blueprint)

    return application