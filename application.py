from app import create_app

application = create_app()

from app.weather import routes
from app.map import routes

if __name__ == "__main__":
    application.run()
